from django.db import models
from typing import Dict, List


HELP_TEXT_AND_VERBOSE_NAME: Dict[str, Dict[str, List[str]]] ={
    'base': {
        'created_at': ['Date of creation', 'Created Date'],
        'updated_at':['Last updated date', 'Last Updated Date'],
        'status': ['is the  object active', 'is_active']
    }
}
class BaseModel(models.Model):
    (
    create_at_,
    update_at_,
    status_,
    ) = HELP_TEXT_AND_VERBOSE_NAME["base"].values()

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=create_at_[1],
        help_text=update_at_[0]

        )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=update_at_[1],
        help_text=update_at_[0]
        )
    status = models.CharField(
        max_length=20, 
        default='active',
        verbose_name=status_[1],
        help_text=status_[0]
        )

    class Meta:
        abstract = True
