from pydantic import BaseModel, Field

class BusinessInput(BaseModel):
    customer_feedback: str = Field(min_length=1, max_length=40000)
    sales_summaries: str = Field(min_length=1, max_length=40000)
    business_type: str = Field(default='SaaS', min_length=1, max_length=100)
    email_tone: str = Field(default='formal', min_length=1, max_length=40)

class Feedback(BaseModel):
    summary: str = Field(min_length=1)
    pain_points: list[str]
    praise: list[str]

class Sales(BaseModel):
    summary: str = Field(min_length=1)
    observations: list[str]
    uncertainties: list[str]

class Insights(BaseModel):
    key_issues: list[str]
    opportunities: list[str]
    customer_behavior_profile: str

class Email(BaseModel):
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)

class Marketing(BaseModel):
    campaign_ideas: list[str]
    content_hooks: list[str]
    product_improvements: list[str]
