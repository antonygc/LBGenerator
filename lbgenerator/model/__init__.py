from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from lbgenerator.model.entities import *
from lbgenerator.lib.generator import BaseMemory
from sqlalchemy.schema import Sequence
from lbgenerator import config
from lbgenerator.model.metabase import HistoryMetaBase
from sqlalchemy.orm import scoped_session

def begin_session():
    """ Returns Session object.
    """
    SESSION = sessionmaker(bind=config.ENGINE, autocommit=True)
    session = scoped_session(SESSION)
    session.begin()
    session.execute('SET datestyle = "ISO, DMY";')
    return session

def base_exists(base_name):
    """ Verify if base exists.
    """
    if not base_name:
        raise Exception('Missing param "nome_base"!')
    if base_name in get_bases():
        return True
    return False

def get_bases():
    """ Get all base names from LB_base
    """
    session = begin_session()
    bases = session.query(LB_Base.nome_base)
    session.close()
    return [base[0] for base in bases.all()]

def make_restful_app():
    """ Initialize Restfull API
    """
    # Create Base table
    config.METADATA.create_all(bind=config.ENGINE, tables=[LB_Base.__table__])

    global BASES
    global HISTORY

    # Create Base Memory
    BASES = BaseMemory(begin_session, LB_Base)

    # Create Base History meta base
    HISTORY = HistoryMetaBase()
    HISTORY.create_base(begin_session)

def reg_hyper_class(base_name, **custom_cols):
    """ Sqla's dynamic mapp (reg table)
    """
    classname = 'LB_Reg_%s' %(base_name)
    reg_table = get_reg_table(base_name, config.METADATA, **custom_cols)

    def reg_next_id():
        """ Get next value from sequence.
        """
        seq = Sequence('lb_reg_%s_id_reg_seq' %(base_name))
        seq.create(bind=config.ENGINE)
        session = begin_session()
        _next = session.execute(seq)
        session.close()
        return _next

    ext = {
        'next_id': reg_next_id,
        'base_name': base_name
    }

    RegHyperClass = type(classname, (RegSuperClass, ), ext)
    mapper(RegHyperClass, reg_table)
    return RegHyperClass

def doc_hyper_class(base_name):
    """ Sqla's dynamic mapp (doc table)
    """
    classname = 'LB_Doc_%s' %(base_name)
    doc_table = get_doc_table(base_name, config.METADATA)

    def doc_next_id():
        """ Get next value from sequence.
        """
        seq = Sequence('lb_doc_%s_id_doc_seq' %(base_name))
        seq.create(bind=config.ENGINE)
        session = begin_session()
        _next = session.execute(seq)
        session.close()
        return _next

    ext = {
        'next_id': doc_next_id,
        'base_name': base_name
    }

    DocHyperClass = type(classname, (DocSuperClass, ), ext)
    mapper(DocHyperClass, doc_table)
    return DocHyperClass

