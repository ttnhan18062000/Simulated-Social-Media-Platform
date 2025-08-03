from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime

from .models import (
    SimUser,
    PersonaProfile,
    UserMentalState,
    UserActionHistory,
    UserReflection,
    UserRelationship,
    UserPreference,
    UserTraitTag,
)


# ---------------------------
# SimUser
# ---------------------------
def get_all_sim_users(session: Session) -> List[SimUser]:
    return session.exec(select(SimUser)).all()


def get_sim_user_by_id(session: Session, sim_user_id: int) -> Optional[SimUser]:
    return session.get(SimUser, sim_user_id)


def create_sim_user(session: Session, sim_user: SimUser) -> SimUser:
    session.add(sim_user)
    session.commit()
    session.refresh(sim_user)
    return sim_user


def update_sim_user_tick(session: Session, sim_user_id: int):
    sim_user = get_sim_user_by_id(session, sim_user_id)
    if sim_user:
        sim_user.tick_count += 1
        session.commit()


# ---------------------------
# PersonaProfile
# ---------------------------
def get_persona(session: Session, sim_user_id: int) -> Optional[PersonaProfile]:
    return session.exec(
        select(PersonaProfile).where(PersonaProfile.sim_user_id == sim_user_id)
    ).first()


def create_or_update_persona(session: Session, data: PersonaProfile) -> PersonaProfile:
    existing = get_persona(session, data.sim_user_id)
    if existing:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(existing, field, value)
    else:
        session.add(data)
    session.commit()
    return data


# ---------------------------
# UserMentalState
# ---------------------------
def get_mental_state(session: Session, sim_user_id: int) -> Optional[UserMentalState]:
    return session.exec(
        select(UserMentalState).where(UserMentalState.sim_user_id == sim_user_id)
    ).first()


def update_mental_state(session: Session, state: UserMentalState) -> UserMentalState:
    existing = get_mental_state(session, state.sim_user_id)
    if existing:
        for field, value in state.dict(exclude_unset=True).items():
            setattr(existing, field, value)
    else:
        session.add(state)
    session.commit()
    return state


# ---------------------------
# UserActionHistory
# ---------------------------
def log_user_action(session: Session, action: UserActionHistory) -> UserActionHistory:
    session.add(action)
    session.commit()
    session.refresh(action)
    return action


def get_recent_actions(
    session: Session, sim_user_id: int, limit: int = 10
) -> List[UserActionHistory]:
    return session.exec(
        select(UserActionHistory)
        .where(UserActionHistory.sim_user_id == sim_user_id)
        .order_by(UserActionHistory.timestamp.desc())
        .limit(limit)
    ).all()


# ---------------------------
# UserReflection
# ---------------------------
def add_reflection(session: Session, reflection: UserReflection) -> UserReflection:
    session.add(reflection)
    session.commit()
    session.refresh(reflection)
    return reflection


def get_reflections(
    session: Session, sim_user_id: int, limit: int = 5
) -> List[UserReflection]:
    return session.exec(
        select(UserReflection)
        .where(UserReflection.sim_user_id == sim_user_id)
        .order_by(UserReflection.timestamp.desc())
        .limit(limit)
    ).all()


# ---------------------------
# UserRelationship
# ---------------------------
def get_relationship(
    session: Session, sim_user_id: int, target_user_id: int
) -> Optional[UserRelationship]:
    return session.exec(
        select(UserRelationship).where(
            (UserRelationship.sim_user_id == sim_user_id)
            & (UserRelationship.target_user_id == target_user_id)
        )
    ).first()


def create_or_update_relationship(
    session: Session, relation: UserRelationship
) -> UserRelationship:
    existing = get_relationship(session, relation.sim_user_id, relation.target_user_id)
    if existing:
        for field, value in relation.dict(exclude_unset=True).items():
            setattr(existing, field, value)
    else:
        session.add(relation)
    session.commit()
    return relation


# ---------------------------
# UserPreference
# ---------------------------
def get_preference(session: Session, sim_user_id: int) -> Optional[UserPreference]:
    return session.exec(
        select(UserPreference).where(UserPreference.sim_user_id == sim_user_id)
    ).first()


def set_preference(session: Session, preference: UserPreference) -> UserPreference:
    existing = get_preference(session, preference.sim_user_id)
    if existing:
        for field, value in preference.dict(exclude_unset=True).items():
            setattr(existing, field, value)
    else:
        session.add(preference)
    session.commit()
    return preference


# ---------------------------
# UserTraitTag
# ---------------------------
def get_tags(session: Session, sim_user_id: int) -> List[UserTraitTag]:
    return session.exec(
        select(UserTraitTag).where(UserTraitTag.sim_user_id == sim_user_id)
    ).all()


def add_trait_tag(session: Session, tag: UserTraitTag) -> UserTraitTag:
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def remove_trait_tag(session: Session, tag_id: int):
    tag = session.get(UserTraitTag, tag_id)
    if tag:
        session.delete(tag)
        session.commit()
