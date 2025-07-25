from api.auth import get_current_user
from api.exceptions.error_403 import NotRightsForUpdateDeleteSN
from api.functions import check_availability_social_network
from database.models.social_network import SocialNetwork
from database.models.users import User
from fastapi import Depends


async def permisson_author_social_network(
        social_network: SocialNetwork = Depends(
            check_availability_social_network
        ),
        current_user: User = Depends(get_current_user),
):

    if social_network.user_id != current_user.id:
        raise NotRightsForUpdateDeleteSN()

    return social_network
