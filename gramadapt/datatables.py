from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol, DataTable, IdCol
from clld.web.datatables.contribution import Contributions
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values, ValueNameCol
from clld.db.models import common
from clld.db.util import get_distinct_values, icontains
from clld.web.util.helpers import map_marker_img, JS_CLLD
from clld.web.util.htmllib import HTML, literal
from clld.web.util import glottolog

from gramadapt import models


class DomainCol(Col):
    def search(self, qs):
        return icontains(self.model_col, qs)


class Rationales(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            DomainCol(
                self,
                'domains',
                model_col=models.Rationale.domains,
                choices=get_distinct_values(models.Question.dom),
            ),
            Col(self, 'questions', model_col=models.Rationale.count_questions),
        ]


class LanguageCol(Col):
    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        obj = self.get_obj(item)
        return HTML.div(
            HTML.a(
                map_marker_img(self.dt.req, obj),
                title='show %s on map' % getattr(obj, 'name', ''),
                href="#map",
                onclick=JS_CLLD.mapShowInfoWindow('map', obj.id),
                class_='btn',
            ) if obj.latitude else '',
            literal('&nbsp;'),
            glottolog.link(self.dt.req, obj.glottocode, label=obj.name) if obj.glottocode else obj.name
        )


class FocusLanguageCol(LanguageCol):
    def get_obj(self, item):
        return item.focus_language


class NeighborLanguageCol(LanguageCol):
    def get_obj(self, item):
        return item.neighbor_language


class Contactsets(Contributions):
    def base_query(self, query):
        return query.filter(common.Contribution.id != 'cldf')

    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            FocusLanguageCol(self, 'focus'),
            NeighborLanguageCol(self, 'neighbor'),
            Col(self, 'respondent', model_col=models.ContactSet.authors),
        ]


class Questions(Parameters):
    def col_defs(self):
        return [
            IdCol(self, 'id', sClass='left'),
            LinkCol(self, 'name'),
            Col(self,
                'domain',
                model_col=models.Question.dom,
                choices=get_distinct_values(models.Question.dom)),
            Col(self,
                'datatype',
                model_col=models.Question.datatype,
                choices=get_distinct_values(models.Question.datatype)),
        ]


class Answers(Values):
    def base_query(self, query):
        query = query.join(common.ValueSet).options(joinedload(common.Value.valueset))

        #if self.language:
        #    query = query.join(ValueSet.parameter)
        #    return query.filter(ValueSet.language_pk == self.language.pk)

        if self.parameter:
            query = query.join(common.ValueSet.contribution)
            query = query.outerjoin(common.DomainElement).options(
                joinedload(common.Value.domainelement))
            return query.filter(common.ValueSet.parameter_pk == self.parameter.pk)

        if self.contribution:
            query = query.join(common.ValueSet.parameter)
            return query.filter(common.ValueSet.contribution_pk == self.contribution.pk)

        return query

    def col_defs(self):
        name_col = ValueNameCol(self, 'value')
        if self.parameter and self.parameter.domain:
            name_col.choices = [de.name for de in self.parameter.domain]

        if self.parameter:
            return [
                LinkCol(self,
                        'contribution',
                        sTitle=self.req.translate('Contribution'),
                        model_col=common.Contribution.name,
                        get_object=lambda i: i.valueset.contribution),
                name_col,
                Col(self, 'comment', model_col=common.Value.description),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
            ]

        if self.contribution:
            return [
                name_col,
                LinkCol(self,
                        'parameter',
                        sTitle=self.req.translate('Parameter'),
                        model_col=common.Parameter.name,
                        get_object=lambda i: i.valueset.parameter),
                Col(self, 'comment', model_col=common.Value.description),
            ]

        return [name_col]


def includeme(config):
    """register custom datatables"""
    config.register_datatable('contributions', Contactsets)
    config.register_datatable('rationales', Rationales)
    config.register_datatable('parameters', Questions)
    config.register_datatable('values', Answers)
