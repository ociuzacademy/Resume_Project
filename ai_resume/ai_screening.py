

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .skill_extractor import extract_skills


# ============================================================
# LOAD AI MODEL
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ============================================================
# SEMANTIC MATCHING
# ============================================================

def semantic_match(resume_text, job_description):
    """
    Calculate semantic similarity between resume and
    job description using Sentence Transformers.

    Returns:
        float: semantic similarity score from 0 to 100
    """

    if not resume_text or not resume_text.strip():
        return 0.0

    if not job_description or not job_description.strip():
        return 0.0

    # Generate embeddings
    resume_embedding = model.encode(
        resume_text,
        convert_to_numpy=True
    )

    job_embedding = model.encode(
        job_description,
        convert_to_numpy=True
    )

    # Calculate cosine similarity
    similarity = cosine_similarity(
        [resume_embedding],
        [job_embedding]
    )[0][0]

    # Convert 0-1 score to percentage
    score = similarity * 100

    # Keep score between 0 and 100
    score = max(0, min(score, 100))

    return round(score, 2)


# ============================================================
# SKILL MATCHING
# ============================================================

def calculate_skill_match(resume_text, job_description):
    """
    Compare skills found in the resume against skills
    required in the job description.

    Returns:
        dictionary containing:
        - score
        - matched_skills
        - missing_skills
        - resume_skills
        - required_skills
    """

    # Extract skills
    resume_skills = set(
        extract_skills(resume_text)
    )

    required_skills = set(
        extract_skills(job_description)
    )

    # Find matching skills
    matched_skills = (
        resume_skills.intersection(
            required_skills
        )
    )

    # Find missing skills
    missing_skills = (
        required_skills.difference(
            resume_skills
        )
    )

    # Calculate skill score
    if not required_skills:

        skill_score = 0.0

    else:

        skill_score = (
            len(matched_skills)
            /
            len(required_skills)
        ) * 100

    return {

        "score": round(skill_score, 2),

        "matched_skills":
            sorted(matched_skills),

        "missing_skills":
            sorted(missing_skills),

        "resume_skills":
            sorted(resume_skills),

        "required_skills":
            sorted(required_skills)

    }


# ============================================================
# FINAL SCREENING SCORE
# ============================================================

def calculate_final_score(
    semantic_score,
    skill_score
):
    """
    Calculate final screening score.

    Weight:
        Semantic similarity = 40%
        Skill matching      = 60%
    """

    final_score = (
        semantic_score * 0.40
        +
        skill_score * 0.60
    )

    return round(final_score, 2)


# ============================================================
# SCREENING RECOMMENDATION
# ============================================================

def get_recommendation(score):
    """
    Generate a screening category based on the
    final score.
    """

    if score >= 80:

        return "Strong Match"

    elif score >= 60:

        return "Moderate Match"

    else:

        return "Low Match"


# ============================================================
# MAIN RESUME SCREENING FUNCTION
# ============================================================

def screen_resume(
    resume_text,
    job_description
):
    """
    Perform complete AI resume screening.

    Parameters:
        resume_text (str):
            Extracted text from candidate resume.

        job_description (str):
            Job description provided by recruiter.

    Returns:
        dict:
            Complete screening result.
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not resume_text:

        raise ValueError(
            "Resume text cannot be empty."
        )

    if not job_description:

        raise ValueError(
            "Job description cannot be empty."
        )

    # --------------------------------------------------------
    # Semantic matching
    # --------------------------------------------------------

    semantic_score = semantic_match(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # Skill matching
    # --------------------------------------------------------

    skill_result = calculate_skill_match(
        resume_text,
        job_description
    )

    skill_score = skill_result["score"]

    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    final_score = calculate_final_score(
        semantic_score,
        skill_score
    )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    recommendation = get_recommendation(
        final_score
    )

    # --------------------------------------------------------
    # Return complete result
    # --------------------------------------------------------

    return {

        "final_score":
            final_score,

        "semantic_score":
            semantic_score,

        "skill_score":
            skill_score,

        "matched_skills":
            skill_result["matched_skills"],

        "missing_skills":
            skill_result["missing_skills"],

        "resume_skills":
            skill_result["resume_skills"],

        "required_skills":
            skill_result["required_skills"],

        "recommendation":
            recommendation

    }


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    # Example resume
    resume_text = """
    I am a Python Developer with experience in
    Machine Learning and Data Science.

    Skills:
    Python
    SQL
    Pandas
    NumPy
    Machine Learning
    TensorFlow
    Scikit-learn
    Git

    I have experience developing machine learning
    models and data analysis applications.
    """

    # Example job description
    job_description = """
    We are looking for a Python Machine Learning Developer.

    Required skills:
    Python
    Machine Learning
    Deep Learning
    TensorFlow
    SQL
    Pandas
    NumPy
    Git
    Docker

    The candidate should have experience developing
    machine learning models and AI applications.
    """

    # Run screening
    result = screen_resume(
        resume_text,
        job_description
    )

    # Display result
    print("\n")
    print("=" * 60)
    print("        AI RESUME SCREENING RESULT")
    print("=" * 60)

    print(
        f"\nFinal Score      : "
        f"{result['final_score']}%"
    )

    print(
        f"Semantic Score   : "
        f"{result['semantic_score']}%"
    )

    print(
        f"Skill Score      : "
        f"{result['skill_score']}%"
    )

    print(
        f"Recommendation   : "
        f"{result['recommendation']}"
    )

    print("\nRequired Skills:")

    for skill in result["required_skills"]:

        print(f"  • {skill}")

    print("\nMatched Skills:")

    for skill in result["matched_skills"]:

        print(f"  ✓ {skill}")

    print("\nMissing Skills:")

    for skill in result["missing_skills"]:

        print(f"  ✗ {skill}")

    print("\nAll Resume Skills:")

    for skill in result["resume_skills"]:

        print(f"  • {skill}")

    print("=" * 60)