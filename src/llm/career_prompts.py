"""
Career-focused prompts for personalized curriculum generation
"""


def get_career_path_prompt(
    target_role: str,
    current_level: str,
    duration_months: int,
    background: str = None,
    preferences: list = None
) -> str:
    """
    Generate career-focused curriculum prompt.
    
    Args:
        target_role: Desired career role (e.g., "Machine Learning Engineer")
        current_level: Current education/experience level
        duration_months: Available timeframe in months
        background: Educational/professional background
        preferences: Learning preferences or constraints
        
    Returns:
        Personalized curriculum generation prompt
    """
    
    prompt_parts = []
    
    # System context
    prompt_parts.append("""You are an expert career counselor and curriculum designer. 
You create personalized learning paths that align with specific career goals, considering 
the learner's background, timeline, and the current industry requirements.""")
    
    # Career goal
    prompt_parts.append(f"""
Create a comprehensive learning curriculum for someone who wants to become a **{target_role}**.

Current Level: {current_level}
Available Time: {duration_months} months
""")
    
    if background:
        prompt_parts.append(f"Background: {background}")
    
    if preferences:
        prompt_parts.append(f"Learning Preferences: {', '.join(preferences)}")
    
    # Structure requirements
    prompt_parts.append("""
The curriculum should be structured into modules/semesters with:
- Industry-relevant courses and skills
- Practical projects that build a portfolio
- Prerequisites properly sequenced
- Clear milestones toward the career goal

IMPORTANT: Return ONLY valid JSON with no markdown formatting.

JSON Format:
{
  "title": "Career Path to [Role]",
  "level": "Professional Development",
  "duration_semesters": [calculated from months],
  "total_credits": [reasonable total],
  "overview": "Overview of the learning path and how it leads to the target role",
  "learning_outcomes": ["outcome 1", "outcome 2", ...],
  "career_paths": ["Primary role and related opportunities"],
  "semesters": [
    {
      "semester_number": 1,
      "total_credits": number,
      "courses": [
        {
          "code": "COURSE101",
          "name": "Course Name",
          "credits": 3,
          "description": "Brief description",
          "prerequisites": [],
          "category": "Core/Elective/Project"
        }
      ]
    }
  ]
}

CRITICAL REQUIREMENTS:
1. Each course must have 1-6 credits only
2. Include practical projects and portfolio-building courses
3. Align content with real job requirements for {target_role}
4. Progress from fundamentals to job-ready skills
5. Include relevant tools, frameworks, and technologies
6. Add capstone/portfolio project in final semester
7. Use proper JSON formatting (double quotes, no trailing commas)

Return only the JSON object.""")
    
    return "\n".join(prompt_parts)


def get_course_recommendation_prompt(
    completed_courses: list,
    interests: list,
    career_goal: str = None
) -> str:
    """
    Generate course recommendations based on progress and interests.
    
    Args:
        completed_courses: List of courses already completed
        interests: Areas of interest
        career_goal: Optional career goal for alignment
        
    Returns:
        Course recommendation prompt
    """
    
    prompt_parts = []
    
    prompt_parts.append("""You are an academic advisor providing personalized course recommendations.""")
    
    prompt_parts.append(f"""
Based on the following information your task is to recommend:

Completed Courses: {', '.join(completed_courses) if completed_courses else 'None (beginner)'}
Interests: {', '.join(interests)}
""")
    
    if career_goal:
        prompt_parts.append(f"Career Goal: {career_goal}")
    
    prompt_parts.append("""
Recommend 5-8 courses that would be most beneficial next. For each course provide:
- Course code and name
- Why it's recommended
- How it builds on completed courses
- How it aligns with interests/career goals

Return recommendations as a JSON array:
[
  {
    "code": "COURSE101",
    "name": "Course Name",
    "credits": 3,
    "reason": "Why this course is recommended",
    "category": "Core/Elective/Project"
  }
]

Use valid JSON format only.""")
    
    return "\n".join(prompt_parts)
