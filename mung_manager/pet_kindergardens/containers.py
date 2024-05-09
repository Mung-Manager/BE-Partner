from dependency_injector import containers, providers

from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)
from mung_manager.pet_kindergardens.selectors.raw_pet_kindergardens import (
    RawPetKindergardenSelector,
)
from mung_manager.pet_kindergardens.services.pet_kindergardens import (
    PetKindergardenService,
)


class PetKindergardenContainer(containers.DeclarativeContainer):
    pet_kindergarden_selector = providers.Factory(PetKindergardenSelector)
    raw_pet_kindergarden_selector = providers.Factory(RawPetKindergardenSelector)
    pet_kindergarden_service = providers.Factory(
        PetKindergardenService,
        pet_kindergarden_selector=pet_kindergarden_selector,
    )
