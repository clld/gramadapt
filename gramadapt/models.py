from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common
from clld.db.models.source import HasSourceNotNullMixin
from clld.db.meta import DBSession

from gramadapt.interfaces import IRationale

#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------

@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    glottocode = Column(Unicode)
    focus = Column(Boolean, default=False)

    @property
    def contactsets(self):
        return [ca.contribution for ca in self.contribution_assocs]


@implementer(interfaces.IContribution)
class ContactSet(CustomModelMixin, common.Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    color = Column(Unicode)
    authors = Column(Unicode)

    def timeframe_comments(self):
        return sorted(list(
            DBSession.query(common.Value)
            .join(common.ValueSet).join(common.Parameter)
            .filter(Question.timeframe_pk != None)
            .filter(Question.datatype == 'Comment')
            .filter(common.Value.name != None)
            .filter(common.ValueSet.contribution_pk == self.pk)
            .options(joinedload(common.Value.valueset).joinedload(common.ValueSet.parameter))
            .all()), key=lambda v: (
                0 if v.valueset.parameter.dom == 'OV' else 1,
                v.valueset.parameter.id))

    def color_rgba(self, opacity=0.5):
        return 'rgba({}, {})'.format(
            ', '.join([str(int(self.color[i:i + 2], 16)) for i in (1, 3, 5)]), opacity)

    @property
    def focus_language(self):
        for la in self.language_assocs:
            if la.language.focus:
                return la.language

    @property
    def neighbor_language(self):
        for la in self.language_assocs:
            if not la.language.focus:
                return la.language


class VarietyContactSet(Base):
    __table_args__ = (
        UniqueConstraint('language_pk', 'contribution_pk'),
    )
    language_pk = Column(Integer, ForeignKey('language.pk'), nullable=False)
    language = relationship(common.Language, backref="contribution_assocs")
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'), nullable=False)
    contribution = relationship(common.Contribution, backref="language_assocs")


@implementer(IRationale)
class Rationale(Base, common.IdNameDescriptionMixin):
    authors = Column(Unicode)
    count_questions = Column(Integer)
    domains = Column(Unicode)

    @property
    def primary_contributors(self):
        return [assoc.contributor for assoc in
                sorted(self.contributor_assocs, key=lambda a: (a.ord, a.contributor.id))]

    @property
    def secondary_contributors(self):
        return []

    @property
    def markdown(self):
        res = []
        for line in self.description.split('\n'):
            if line.startswith('# '):
                continue
            if line.startswith('## References'):
                continue
            if line.startswith('Authors:'):
                continue
            if line.startswith('#'):
                line = '#' + line
            res.append(line)
        return '\n'.join(res)


class RationaleReference(Base, HasSourceNotNullMixin):
    __table_args__ = (
        UniqueConstraint('rationale_pk', 'source_pk', 'description'),
    )
    rationale_pk = Column(Integer, ForeignKey('rationale.pk'), nullable=False)
    rationale = relationship(Rationale, innerjoin=True, backref="references")


class RationaleContributor(Base):

    """Many-to-many association between contributors and contributions."""

    __table_args__ = (UniqueConstraint('contributor_pk', 'rationale_pk'),)

    contributor_pk = Column(Integer, ForeignKey('contributor.pk'), nullable=False)
    rationale_pk = Column(Integer, ForeignKey('rationale.pk'), nullable=False)

    # contributors are ordered.
    ord = Column(Integer, default=1)

    rationale = relationship(Rationale, innerjoin=True, backref='contributor_assocs')
    contributor = relationship(
        common.Contributor, innerjoin=True, lazy=False, backref='rationale_assocs')


@implementer(interfaces.IParameter)
class Question(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    question_group = Column(Unicode)
    datatype = Column(Unicode)
    dom = Column(Unicode)
    count = Column(Integer)
    domain_rationale_pk = Column(Integer, ForeignKey('rationale.pk'))
    domain_rationale = relationship(
        Rationale,
        foreign_keys=[domain_rationale_pk],
        backref='domain_questions')
    rationale_pk = Column(Integer, ForeignKey('rationale.pk'))
    rationale = relationship(
        Rationale,
        foreign_keys=[rationale_pk],
        backref='questions')
    timeframe_pk = Column(Integer, ForeignKey('question.pk'))
    timeframe = relationship('Question', remote_side=[pk], foreign_keys=[timeframe_pk])

    @property
    def minimum(self):
        if not self.datatype == 'Value':
            return
        return min(vs.jsondata['start'] for vs in self.valuesets)

    @property
    def maximum(self):
        if not self.datatype == 'Value':
            return
        return max(vs.jsondata['end'] for vs in self.valuesets)

    def iter_ranges(self):
        if not self.datatype == 'Value':
            return
        e = max(vs.jsondata['end'] for vs in self.valuesets)
        s = min(vs.jsondata['start'] for vs in self.valuesets)

        def percent(year):
            return (year - s) / (e - s) * 100

        for vs in self.valuesets:
            yield vs, percent(vs.jsondata['start']) - 0.15, percent(vs.jsondata['end'] - vs.jsondata['start'] + s) - 0.15
