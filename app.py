import streamlit as st
import html

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at top left,
            rgba(99, 102, 241, 0.18),
            transparent 35%
        ),
        radial-gradient(
            circle at bottom right,
            rgba(168, 85, 247, 0.16),
            transparent 35%
        ),
        #080b18;
}

/* Main container */

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   TEXT
   ============================================================ */

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

p {
    color: #cbd5e1;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {
    background: linear-gradient(
        135deg,
        #4338ca,
        #7c3aed
    );

    border-radius: 24px;

    padding: 42px;

    margin-bottom: 30px;

    border: 1px solid rgba(255,255,255,0.15);

    box-shadow:
        0 25px 60px rgba(0,0,0,0.35);
}

.hero-badge {
    display: inline-block;

    background: rgba(255,255,255,0.15);

    color: #ffffff;

    padding: 7px 14px;

    border-radius: 50px;

    font-size: 13px;

    font-weight: 600;

    margin-bottom: 15px;
}

.hero-title {
    color: #ffffff;

    font-size: 42px;

    font-weight: 800;

    margin-bottom: 10px;
}

.hero-description {
    color: #e0e7ff;

    font-size: 16px;

    line-height: 1.6;
}


/* ============================================================
   PIPELINE
   ============================================================ */

.pipeline-card {
    background: rgba(255,255,255,0.055);

    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 18px;

    padding: 20px;

    min-height: 175px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.20);
}

.pipeline-icon {
    font-size: 28px;

    margin-bottom: 12px;
}

.pipeline-title {
    color: #ffffff;

    font-size: 17px;

    font-weight: 700;

    margin-bottom: 8px;
}

.pipeline-description {
    color: #94a3b8;

    font-size: 13px;

    line-height: 1.5;
}


/* ============================================================
   STATUS
   ============================================================ */

.status {
    display: inline-block;

    margin-top: 15px;

    padding: 5px 10px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 700;
}

.status-pending {
    background: rgba(148,163,184,0.12);

    color: #cbd5e1;
}

.status-running {
    background: rgba(59,130,246,0.15);

    color: #93c5fd;
}

.status-done {
    background: rgba(34,197,94,0.15);

    color: #86efac;
}


/* ============================================================
   RESULT CARD
   ============================================================ */

.result-card {
    background: rgba(255,255,255,0.045);

    border: 1px solid rgba(255,255,255,0.09);

    border-radius: 18px;

    padding: 25px;

    margin-top: 20px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #090d1a;

    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0;
}


/* ============================================================
   INPUT
   ============================================================ */

textarea {
    background: #111827 !important;

    color: #ffffff !important;

    border: 1px solid #334155 !important;

    border-radius: 12px !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {
    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    color: white !important;

    border: none;

    border-radius: 12px;

    padding: 12px;

    font-weight: 700;
}

.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );
}


/* ============================================================
   DOWNLOAD
   ============================================================ */

.stDownloadButton > button {
    background: rgba(255,255,255,0.07);

    color: white !important;

    border: 1px solid rgba(255,255,255,0.15);

    border-radius: 12px;
}


/* ============================================================
   EXPANDER
   ============================================================ */

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 12px;
}


/* ============================================================
   METRICS
   ============================================================ */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.08);

    padding: 15px;

    border-radius: 14px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# PIPELINE STATUS FUNCTION
# ============================================================

def show_pipeline(status):

    stages = [
        (
            "search",
            "🔎",
            "Search Agent",
            "Find relevant and reliable information from the web.",
        ),
        (
            "reader",
            "📖",
            "Reader Agent",
            "Select and scrape the most useful source.",
        ),
        (
            "writer",
            "✍️",
            "Writer Chain",
            "Generate a structured research report.",
        ),
        (
            "critic",
            "🧐",
            "Critic Chain",
            "Review the generated research report.",
        ),
    ]

    columns = st.columns(4)

    for column, stage in zip(columns, stages):

        key, icon, title, description = stage

        current_status = status[key]

        if current_status == "running":
            status_text = "🔵 Running"
            status_class = "status-running"

        elif current_status == "done":
            status_text = "🟢 Completed"
            status_class = "status-done"

        else:
            status_text = "⚪ Pending"
            status_class = "status-pending"

        # IMPORTANT:
        # HTML starts at column 0.
        # No indentation before <div>.
        card = f"""<div class="pipeline-card">
<div class="pipeline-icon">{icon}</div>
<div class="pipeline-title">{title}</div>
<div class="pipeline-description">{description}</div>
<div class="status {status_class}">{status_text}</div>
</div>"""

        with column:
            st.markdown(
                card,
                unsafe_allow_html=True,
            )


# ============================================================
# HERO
# ============================================================

hero = """<div class="hero-box">
<div class="hero-badge">🤖 Multi-Agent Research System</div>
<div class="hero-title">🔬 AI Research Agent</div>
<div class="hero-description">
Search the web → Read sources → Write a report → Critically review
</div>
</div>"""

st.markdown(
    hero,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## ⚙️ Research Settings"
    )

    topic = st.text_area(
        "Research Topic",
        placeholder=(
            "Example:\n"
            "Impact of generative AI on software development"
        ),
        height=150,
    )

    st.markdown("---")

    st.markdown(
        "### 🧠 Pipeline Architecture"
    )

    st.markdown(
        """
        **🔎 Search Agent**

        Finds relevant web resources.

        **📖 Reader Agent**

        Scrapes useful information.

        **✍️ Writer Chain**

        Creates the research report.

        **🧐 Critic Chain**

        Reviews the final report.
        """
    )

    st.markdown("---")

    start = st.button(
        "🚀 Start Research",
        use_container_width=True,
    )


# ============================================================
# PIPELINE HEADER
# ============================================================

st.markdown(
    "## ⚡ Pipeline Status"
)


# ============================================================
# INITIAL STATUS
# ============================================================

status = {
    "search": "pending",
    "reader": "pending",
    "writer": "pending",
    "critic": "pending",
}


pipeline_placeholder = st.empty()


def refresh_pipeline():

    with pipeline_placeholder.container():

        show_pipeline(status)


refresh_pipeline()


# ============================================================
# RUN PIPELINE
# ============================================================

if start:

    if not topic.strip():

        st.warning(
            "Please enter a research topic."
        )

        st.stop()


    progress = st.progress(0)

    message = st.empty()


    # ========================================================
    # SEARCH
    # ========================================================

    status["search"] = "running"

    refresh_pipeline()

    message.info(
        "🔎 Search Agent is finding reliable sources..."
    )

    try:

        search_agent = build_search_agent()

        search_response = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Find recent, reliable and detailed information about: {topic}",
                    )
                ]
            }
        )

        search_results = (
            search_response["messages"][-1].content
        )

        status["search"] = "done"

        progress.progress(25)

    except Exception as error:

        status["search"] = "pending"

        refresh_pipeline()

        st.error(
            f"Search Agent failed: {error}"
        )

        st.stop()


    refresh_pipeline()


    # ========================================================
    # READER
    # ========================================================

    status["reader"] = "running"

    refresh_pipeline()

    message.info(
        "📖 Reader Agent is scraping the best source..."
    )

    try:

        reader_agent = build_reader_agent()

        reader_response = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        (
                            f"Based on these search results about "
                            f"'{topic}', pick the most relevant URL "
                            "and scrape it for deeper content.\n\n"
                            f"Search Results:\n{search_results[:800]}"
                        ),
                    )
                ]
            }
        )

        scraped_content = (
            reader_response["messages"][-1].content
        )

        status["reader"] = "done"

        progress.progress(50)

    except Exception as error:

        status["reader"] = "pending"

        refresh_pipeline()

        st.error(
            f"Reader Agent failed: {error}"
        )

        st.stop()


    refresh_pipeline()


    # ========================================================
    # WRITER
    # ========================================================

    status["writer"] = "running"

    refresh_pipeline()

    message.info(
        "✍️ Writer Chain is creating the report..."
    )

    try:

        research = (
            "SEARCH RESULTS:\n\n"
            f"{search_results}\n\n"
            "SCRAPED CONTENT:\n\n"
            f"{scraped_content}"
        )

        report = writer_chain.invoke(
            {
                "topic": topic,
                "research": research,
            }
        )

        status["writer"] = "done"

        progress.progress(75)

    except Exception as error:

        status["writer"] = "pending"

        refresh_pipeline()

        st.error(
            f"Writer Chain failed: {error}"
        )

        st.stop()


    refresh_pipeline()


    # ========================================================
    # CRITIC
    # ========================================================

    status["critic"] = "running"

    refresh_pipeline()

    message.info(
        "🧐 Critic Chain is reviewing the report..."
    )

    try:

        feedback = critic_chain.invoke(
            {
                "report": report,
            }
        )

        status["critic"] = "done"

        progress.progress(100)

        message.success(
            "🎉 Research pipeline completed!"
        )

    except Exception as error:

        status["critic"] = "pending"

        refresh_pipeline()

        st.error(
            f"Critic Chain failed: {error}"
        )

        st.stop()


    refresh_pipeline()


    # ========================================================
    # REPORT
    # ========================================================

    st.markdown("---")

    st.markdown(
        "## 📄 Research Report"
    )

    st.markdown(
        f"""<div class="result-card">
<h3>{html.escape(topic)}</h3>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(report)


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.markdown("---")

    st.markdown(
        "## 📥 Download Results"
    )

    safe_name = (
        topic
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "⬇️ Download Research Report",
            data=report,
            file_name=f"{safe_name}_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:

        st.download_button(
            "⬇️ Download Critic Feedback",
            data=feedback,
            file_name=f"{safe_name}_critic.txt",
            mime="text/plain",
            use_container_width=True,
        )


    # ========================================================
    # CRITIC
    # ========================================================

    st.markdown("---")

    st.markdown(
        "## 🧐 Critic Analysis"
    )

    with st.expander(
        "View critic feedback",
        expanded=True,
    ):

        st.markdown(feedback)


    # ========================================================
    # RAW SEARCH
    # ========================================================

    with st.expander(
        "🔎 View Search Results"
    ):

        st.text(search_results)


    # ========================================================
    # SCRAPED CONTENT
    # ========================================================

    with st.expander(
        "📖 View Scraped Content"
    ):

        st.text(scraped_content)


    # ========================================================
    # SUMMARY
    # ========================================================

    st.markdown("---")

    st.markdown(
        "## 📊 Pipeline Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🔎 Search",
            "Done",
        )

    with col2:
        st.metric(
            "📖 Reader",
            "Done",
        )

    with col3:
        st.metric(
            "✍️ Writer",
            "Done",
        )

    with col4:
        st.metric(
            "🧐 Critic",
            "Done",
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div style="
    text-align:center;
    color:#64748b;
    padding:40px 0 10px 0;
    font-size:13px;
">
AI Research Agent
<br>
Search • Scraping • Writing • Criticism
</div>
""",
    unsafe_allow_html=True,
)