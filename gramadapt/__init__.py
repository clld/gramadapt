import collections

from pyramid.config import Configurator
from clld.interfaces import IMapMarker, IValueSet, IValue, IDomainElement, ILanguage
from clld.web.icon import MapMarker
from clldutils.svg import pie, icon, data_url

# we must make sure custom models are known at database initialization!
from gramadapt import models
from gramadapt.interfaces import IRationale


_ = lambda s: s
_('Contribution')
_('Contributions')
_('Parameter')
_('Parameters')


class FeatureMapMarker(MapMarker):
    def __call__(self, ctx, req):
        if IValueSet.providedBy(ctx):
            if len(ctx.values) == 1:
                return data_url(icon(ctx.values[0].domainelement.jsondata['icon']))
            c = collections.Counter([v.domainelement.jsondata['icon'] for v in ctx.values])
            return data_url(pie(*list(zip(*[(v, k[1:]) for k, v in c.most_common()])), **dict(stroke_circle=True)))
        if IDomainElement.providedBy(ctx):
            return data_url(icon(ctx.jsondata['icon']))
        if IValue.providedBy(ctx):
            return data_url(icon(ctx.domainelement.jsondata['icon']))
        if ILanguage.providedBy(ctx):
            return data_url(icon('{}{}'.format('c' if ctx.focus else 'd', ctx.contactsets[0].color[1:])))
        return super(FeatureMapMarker, self).__call__(ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['clld_markdown_plugin'] = {
        'keep_link_labels': True,
    }
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.include('clldmpg')
    config.include('clld_markdown_plugin')
    config.register_resource('rationale', models.Rationale, IRationale, with_index=True)

    config.registry.registerUtility(FeatureMapMarker(), IMapMarker)

    return config.make_wsgi_app()
