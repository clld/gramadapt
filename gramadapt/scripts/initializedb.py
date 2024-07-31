import re
import itertools
import collections

from clldutils.misc import nfilter
from clldutils.color import qualitative_colors, sequential_colors, diverging_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from matplotlib import colormaps
from matplotlib.colors import rgb2hex

from pycldf import Sources

import gramadapt
from gramadapt import models


def main(args):
    data = Data()
    ds = data.add(
        common.Dataset,
        gramadapt.__name__,
        id=gramadapt.__name__,
        domain='',
        name=args.cldf.properties['dc:title'],
        description=args.cldf.properties['dc:description'],
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},

    )
    for i, row in enumerate(args.cldf.iter_rows('contributors.csv')):
        c = data.add(
            common.Contributor,
            row['ID'],
            id=row['ID'],
            name=row['Name'])
        if row['Editor']:
            DBSession.add(common.Editor(dataset=ds, ord=i + 1, contributor=c))
    DBSession.add(common.Editor(
        dataset=ds, ord=i + 2, contributor=common.Contributor(id='forkel', name='Robert Forkel')))

    colors = qualitative_colors(34)

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    for c in args.cldf.objects('ContributionTable'):
        if c.data['Type'] == 'rationale':
            r = data.add(
                models.Rationale,
                c.id,
                id=c.id,
                name=c.cldf.name,
                description=c.cldf.description,
                authors=c.cldf.contributor,
            )
            for ref in c.references:
                DBSession.add(
                    models.RationaleReference(rationale=r, source=data['Source'][ref.source.id]))
            cls, kw = models.RationaleContributor, {'rationale': r}
        else:
            r = data.add(
                models.ContactSet,
                c.id,
                id=c.id,
                name=c.cldf.name,
                authors=c.cldf.contributor,
                color=colors.pop()
            )
            cls, kw = common.ContributionContributor, {'contribution': r}
        for i, cid in enumerate(c.data['Author_IDs']):
            DBSession.add(cls(contributor=data['Contributor'][cid], ord=i + 1, **kw))

    question_groups = {r['ID']: r for r in args.cldf.iter_rows('questions.csv')}

    # Merge parameters F and S into a language property which can be used to inform map markers.
    for lang in args.cldf.iter_rows('LanguageTable', 'id', 'glottocode', 'name', 'latitude', 'longitude'):
        data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['glottocode'],
        )

    for v in args.cldf.iter_rows('ValueTable'):
        if v['Parameter_ID'] == 'F' and v['Value'] == 'Yes':
            data['Variety'][v['Language_ID']].focus = True
        if v['Parameter_ID'] == 'S':
            data['Variety'][v['Language_ID']].contactset = data['ContactSet'][v['Contactset_ID']]

    refs = collections.defaultdict(list)

    #
    # FIXME: store the contact pair data in such a way that it can be displayed as one parameter!
    #

    #
    # load time ranges as one parameter, with an artificial domain, color code
    # colors.rgb2hex(colormaps['Greens'](0)[:3])
    # Param ID endswith('N0') or N1
    ranges, range_comments = {}, {}
    for param in args.cldf.objects('ParameterTable'):
        if param.id.endswith('N0'):
            ranges[param.id[:-2]] = collections.defaultdict(list)
            range_comments[param.id[:-2]] = {}

    for param in args.cldf.iter_rows('ParameterTable', 'id', 'name'):
        if param['id'] in {'S', 'F'}:
            continue
        if param['id'].endswith('N0') or param['id'].endswith('N1'):
            continue
        rationale = question_groups.get(param['Question_ID'], {}).get('Rationale')
        data.add(
            models.Question,
            param['id'],
            id=param['id'],
            name='{}'.format(param['name']),
            datatype=param['datatype'],
            rationale=data['Rationale'].get(rationale),
            dom=param['Domain'],
    )

    for pid, codes in itertools.groupby(
        sorted(
            args.cldf.objects('CodeTable'),
            key=lambda v: (
                    v.cldf.parameterReference,
                    v.data['Ordinal'] or 99,
                    re.sub(r'-B$', '-zz', v.id))),
        lambda v: v.cldf.parameterReference,
    ):
        codes = list(codes)
        param = codes[0].parameter
        if param.id in {'S', 'F'}:
            continue
        assert codes[-1].cldf.name == 'B', '{}: {}'.format(param.id, [c.cldf.name for c in codes])
        if param.data['datatype'] == 'Scalar':
            colors = diverging_colors(len(codes) - 1)
        elif param.data['datatype'] == 'TypesSequential':
            colors = sequential_colors(len(codes) - 1)
        else:
            colors = qualitative_colors(len(codes) - 1)
        for code, color in zip(codes, colors + ['#000000']):
            data.add(
                common.DomainElement,
                code.id,
                id=code.id,
                name=code.cldf.name,
                description=code.cldf.description,
                parameter=data['Question'][param.id],
                jsondata=dict(icon=('c' if code.cldf.name != 'B' else 't') + color.replace('#', '')),
            )

    for val in args.cldf.iter_rows(
            'ValueTable',
            'id', 'value', 'languageReference', 'parameterReference', 'codeReference', 'source'):
        if val['value'] is None:  # Missing values are ignored.
            continue
        if val['parameterReference'] in {'S', 'F'}:
            continue

        if val['parameterReference'][-2:] in {'N0', 'N1'}:
            ranges[val['parameterReference'][:-2]][val['Contactset_ID']].append(val)
            continue

        if val['parameterReference'] in range_comments:
            range_comments[val['parameterReference']][val['Contactset_ID']] = val['value']

        vsid = (val['languageReference'], val['parameterReference'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                language=data['Variety'][val['languageReference']],
                parameter=data['Question'][val['parameterReference']],
                contribution=data['ContactSet'][val['Contactset_ID']],
            )
        for ref in val.get('source', []):
            sid, pages = Sources.parse(ref)
            refs[(vsid, sid)].append(pages)
        data.add(
            common.Value,
            val['id'],
            id=val['id'],
            name=val['value'],
            valueset=vs,
            domainelement=data['DomainElement'][val['codeReference']] if val['codeReference'] else None,
            description=val['Comment'],
        )
    #
    # Now insert data for time ranges!
    #
    cm = colormaps['Greens']
    for pid, values in ranges.items():
        assert all(len(v) == 2 for _, v in values.items())
        middles = {}
        for setid, vals in values.items():
            middles[setid] = sum(int(v['Value']) for v in vals) / 2
        minimum = min(middles.values())
        maximun = max(middles.values())
        #
        #
        #
        param = data['Question'][pid]
        p = data.add(
            models.Question,
            pid + 'N',
            id=pid + 'N',
            name=param.name + ' Coarse time range',
            datatype='Value',
            rationale=param.rationale,
            dom=param.dom,
        )
        for sid, vals in values.items():
            # create a domainelement, with appropriately colored icon!
            vals = sorted(vals, key=lambda i: int(i['Value']))
            fmt = lambda n: ('present' if n >= 2020 else str(n)) if n > 0 \
                else '{}BP'.format(n - 1950).replace('-', '')
            n = '{}-{}'.format(fmt(int(vals[0]['Value'])), fmt(int(vals[1]['Value'])))
            cid = '{}N{}'.format(pid, n)
            de = data['DomainElement'].get(cid)
            if not de:
                de = data.add(
                    common.DomainElement,
                    cid,
                    id=cid,
                    name=n,
                    description=None,
                    parameter=data['Question'][param.id],
                    jsondata=dict(icon=('c' + rgb2hex(cm((middles[sid] - minimum) / (maximun - minimum))))),
                )
            vs = data.add(
                common.ValueSet,
                '{}N{}'.format(pid, sid),
                id='{}N{}'.format(pid, sid),
                language=data['Variety'][vals[0]['languageReference']],
                parameter=p,
                contribution=data['ContactSet'][sid],
                jsondata=dict(
                    comment=range_comments[pid].get(sid, ''),
                    start=int(vals[0]['Value']),
                    end=int(vals[1]['Value'])),
            )
            data.add(
                common.Value,
                '{}N{}'.format(pid, sid),
                id='{}N{}'.format(pid, sid),
                name=n,
                valueset=vs,
                domainelement=de,
            )

    for (vsid, sid), pages in refs.items():
        DBSession.add(common.ValueSetReference(
            valueset=data['ValueSet'][vsid],
            source=data['Source'][sid],
            description='; '.join(nfilter(pages))
        ))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for r in DBSession.query(models.Rationale):
        r.count_questions = len(r.questions)
        r.domains = ' '.join(sorted({q.dom for q in r.questions if q.dom}))

    for q in DBSession.query(models.Question):
        q.count = len(q.valuesets)