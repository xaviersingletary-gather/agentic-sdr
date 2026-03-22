import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.account import Account, AccountStatus
from src.models.contact import Contact, PersonaType, OutreachStatus
from src.models.signal import Signal, SignalType, SignalSource, SIGNAL_POINTS
from src.models.outreach import Outreach, Channel, SEQUENCE_DAYS


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_account_create_read_update_delete(db):
    account = Account(company_name="Acme Logistics", domain="acme.com", industry="Logistics",
                      annual_revenue=750_000_000, facility_count=15, hq_country="US")
    db.add(account)
    db.commit()
    fetched = db.query(Account).filter_by(company_name="Acme Logistics").first()
    assert fetched is not None
    assert fetched.annual_revenue == 750_000_000
    fetched.status = AccountStatus.qualified
    db.commit()
    assert db.query(Account).filter_by(status=AccountStatus.qualified).count() == 1
    db.delete(fetched)
    db.commit()
    assert db.query(Account).count() == 0


def test_contact_create_read_update_delete(db):
    account = Account(company_name="Acme Logistics")
    db.add(account)
    db.commit()
    contact = Contact(account_id=account.id, first_name="Jane", last_name="Doe",
                      title="Director of Continuous Improvement", persona_type=PersonaType.tdm,
                      email="jane.doe@acme.com", verified=True)
    db.add(contact)
    db.commit()
    fetched = db.query(Contact).filter_by(email="jane.doe@acme.com").first()
    assert fetched.persona_type == PersonaType.tdm
    assert fetched.verified is True
    fetched.outreach_status = OutreachStatus.enrolled
    db.commit()
    assert db.query(Contact).filter_by(outreach_status=OutreachStatus.enrolled).count() == 1
    db.delete(fetched)
    db.commit()
    assert db.query(Contact).count() == 0


def test_signal_create_read_update_delete(db):
    account = Account(company_name="Acme Logistics")
    db.add(account)
    db.commit()
    signal = Signal(account_id=account.id, signal_type=SignalType.job_posting,
                    signal_source=SignalSource.clay,
                    raw_content="Hiring Director of Inventory Control",
                    points_contributed=SIGNAL_POINTS[SignalType.job_posting])
    db.add(signal)
    db.commit()
    fetched = db.query(Signal).filter_by(signal_type=SignalType.job_posting).first()
    assert fetched.points_contributed == 25
    db.delete(fetched)
    db.commit()
    assert db.query(Signal).count() == 0


def test_outreach_create_read_update_delete(db):
    account = Account(company_name="Acme Logistics")
    db.add(account)
    db.commit()
    contact = Contact(account_id=account.id, first_name="Jane", email="jane@acme.com")
    db.add(contact)
    db.commit()
    outreach = Outreach(contact_id=contact.id, account_id=account.id,
                        channel=Channel.email, sequence_day=0, template_id="tdm_day0")
    db.add(outreach)
    db.commit()
    fetched = db.query(Outreach).filter_by(sequence_day=0).first()
    assert fetched.channel == Channel.email
    db.delete(fetched)
    db.commit()
    assert db.query(Outreach).count() == 0


def test_sequence_days_are_correct():
    assert SEQUENCE_DAYS == [0, 3, 7, 14, 30]


def test_signal_points_mapping():
    assert SIGNAL_POINTS[SignalType.job_posting] == 25
    assert SIGNAL_POINTS[SignalType.new_dc] == 25
    assert SIGNAL_POINTS[SignalType.wms_migration] == 20
    assert SIGNAL_POINTS[SignalType.audit_failure] == 20
    assert SIGNAL_POINTS[SignalType.automation_adoption] == 10
    assert SIGNAL_POINTS[SignalType.exec_mandate] == 20
