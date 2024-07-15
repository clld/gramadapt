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
    contactset_pk = Column(Integer, ForeignKey('contribution.pk'))
    contactset = relationship(common.Contribution, backref='languages')


@implementer(interfaces.IContribution)
class ContactSet(CustomModelMixin, common.Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    color = Column(Unicode)
    authors = Column(Unicode)

    def timeframe_comments(self):
        return list(
            DBSession.query(common.Value)
            .join(common.ValueSet).join(common.Parameter).join(Rationale)
            .filter(Rationale.id.in_(['P1', 'P2', 'P3']))
            .filter(Question.datatype == 'Comment')
            .filter(common.Value.name != None)
            .filter(common.ValueSet.contribution_pk == self.pk)
            .options(joinedload(common.Value.valueset).joinedload(common.ValueSet.parameter))
            .all())

    @property
    def focus_language(self):
        for l in self.languages:
            if l.focus:
                return l

    @property
    def neighbor_language(self):
        for l in self.languages:
            if not l.focus:
                return l


@implementer(IRationale)
class Rationale(Base, common.IdNameDescriptionMixin):
    authors = Column(Unicode)
    count_questions = Column(Integer)
    domains = Column(Unicode)


class RationaleReference(Base, HasSourceNotNullMixin):
    __table_args__ = (
        UniqueConstraint('rationale_pk', 'source_pk', 'description'),
    )
    rationale_pk = Column(Integer, ForeignKey('rationale.pk'), nullable=False)
    rationale = relationship(Rationale, innerjoin=True, backref="references")


@implementer(interfaces.IParameter)
class Question(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    question_group = Column(Unicode)
    datatype = Column(Unicode)
    dom = Column(Unicode)
    #
    # FIXME: link to rationale
    #
    rationale_pk = Column(Integer, ForeignKey('rationale.pk'))
    rationale = relationship(Rationale, backref='questions')
