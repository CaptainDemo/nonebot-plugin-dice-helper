from pydantic import BaseModel

class DiceHelperConfig(BaseModel):
    dice_helper_use_prefix_variance: bool = False
