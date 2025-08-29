"""
ISSA Theme Configuration - Professional Finance Palette
Theme configuration file for ISSA dashboards
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

class ISSATheme:
    """ISSA Dashboard Theme Configuration - Professional Finance Edition"""
    
    # Professional Finance/ISSA Color Palette
    PALETTE = {
        # Layout Colors
        "primary_bg": "#F6F8FA",     # Neutral, calm base background
        "sidebar_bg": "#223A5E",     # Deep navy for left panel/sidebar
        "card_bg": "#FFFFFF",        # Main/metric cards and tables
        "divider": "#E3E7EC",        # Section separators
        
        # Font Colors
        "font_main": "#222D37",      # Main dashboard body text, dark navy
        "font_heading": "#17479E",   # Headings/tabs, strong blue
        "font_sidebar": "#F6F8FA",   # White/soft gray sidebar text
        
        # Accent/Brand Colors
        "accent": "#288FFA",         # Primary accent (buttons, active tab, highlights)
        "accent2": "#4FC3F7",        # Secondary accent (hover, tabs, badges)
        
        # Status Colors (KPIs, Charts, Alerts)
        "success": "#2E865F",        # For positive/financial improvement
        "warning": "#F7B731",        # Orange for cautions, 'Warning' status
        "error": "#D62728",          # Red for 'Overrun', errors, critical
        "info": "#0095C9",           # Used for informational content, non-KPI blue
        "inactive": "#BFC9D1",       # Disabled or faded controls, muted
        
        # Highlight/Selection
        "highlight": "#E8FAF4",      # For selected rows, focus effects
    }
    
    # Typography
    FONT_FAMILY = "'Open Sans', 'Roboto', 'Arial', sans-serif"
    FONT_FAMILY_HEADING = "'Montserrat', 'Roboto', 'Arial', sans-serif"
    
    @classmethod
    def get_css(cls):
        """Generate CSS for Streamlit styling with improved colors"""
        return f"""
        <style>
        /* Global Styles */
        .stApp {{
            font-family: {cls.FONT_FAMILY};
            color: {cls.PALETTE['font_main']};
            background-color: {cls.PALETTE['primary_bg']};
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            font-family: {cls.FONT_FAMILY_HEADING};
            color: {cls.PALETTE['font_heading']};
            font-weight: 700;
        }}
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: {cls.PALETTE['sidebar_bg']};
        }}
        
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {{
            color: {cls.PALETTE['font_sidebar']} !important;
        }}
        
        /* Metric Cards */
        [data-testid="metric-container"] {{
            background-color: {cls.PALETTE['card_bg']};
            border: 1px solid {cls.PALETTE['divider']};
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        
        /* Success Box */
        .success-box {{
            background-color: {cls.PALETTE['highlight']};
            border-left: 4px solid {cls.PALETTE['success']};
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
            color: {cls.PALETTE['font_main']};
        }}
        
        /* Warning Box */
        .warning-box {{
            background-color: #FFF8E1;
            border-left: 4px solid {cls.PALETTE['warning']};
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
            color: {cls.PALETTE['font_main']};
        }}
        
        /* Error Box */
        .error-box {{
            background-color: #FFEBEE;
            border-left: 4px solid {cls.PALETTE['error']};
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
            color: {cls.PALETTE['font_main']};
        }}
        
        /* Info Box */
        .info-box {{
            background-color: {cls.PALETTE['card_bg']};
            border-left: 4px solid {cls.PALETTE['info']};
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            color: {cls.PALETTE['font_main']};
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {cls.PALETTE['accent']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            font-family: {cls.FONT_FAMILY};
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background-color: {cls.PALETTE['accent2']};
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transform: translateY(-1px);
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            border-bottom: 2px solid {cls.PALETTE['divider']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: {cls.PALETTE['card_bg']};
            color: {cls.PALETTE['font_main']};
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: 600;
            font-family: {cls.FONT_FAMILY};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {cls.PALETTE['accent']};
            color: white;
        }}
        
        /* Dashboard Header */
        .dashboard-header {{
            background: linear-gradient(135deg, {cls.PALETTE['sidebar_bg']} 0%, {cls.PALETTE['accent']} 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}
        
        /* Section Headers */
        .section-header {{
            background-color: {cls.PALETTE['card_bg']};
            padding: 15px 20px;
            border-radius: 8px;
            border-left: 5px solid {cls.PALETTE['accent']};
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            color: {cls.PALETTE['font_heading']};
        }}
        </style>
        """
    
    @classmethod
    def setup_plotly_theme(cls):
        """Configure Plotly theme with improved finance colors"""
        pio.templates["issa_finance"] = go.layout.Template(
            layout=go.Layout(
                paper_bgcolor=cls.PALETTE["primary_bg"],
                plot_bgcolor=cls.PALETTE["card_bg"],
                font=dict(
                    family=cls.FONT_FAMILY,
                    color=cls.PALETTE["font_main"],
                    size=14
                ),
                title=dict(
                    font=dict(
                        family=cls.FONT_FAMILY_HEADING,
                        size=22,
                        color=cls.PALETTE["font_heading"]
                    )
                ),
                colorway=[
                    cls.PALETTE["accent"], 
                    cls.PALETTE["success"],
                    cls.PALETTE["warning"], 
                    cls.PALETTE["error"],
                    cls.PALETTE["info"],
                    cls.PALETTE["accent2"],
                    cls.PALETTE["inactive"]
                ],
                xaxis=dict(
                    gridcolor=cls.PALETTE["divider"],
                    tickfont=dict(color=cls.PALETTE["font_main"]),
                    title_font=dict(color=cls.PALETTE["font_main"])
                ),
                yaxis=dict(
                    gridcolor=cls.PALETTE["divider"],
                    tickfont=dict(color=cls.PALETTE["font_main"]),
                    title_font=dict(color=cls.PALETTE["font_main"])
                ),
                hoverlabel=dict(
                    bgcolor=cls.PALETTE["card_bg"],
                    bordercolor=cls.PALETTE["accent"],
                    font_size=14,
                    font_family=cls.FONT_FAMILY,
                    font_color=cls.PALETTE["font_main"]
                )
            )
        )
        pio.templates.default = "issa_finance"
    
    @classmethod
    def apply_theme(cls):
        """Apply complete theme to Streamlit app"""
        st.markdown(cls.get_css(), unsafe_allow_html=True)
        cls.setup_plotly_theme()
    
    @classmethod
    def get_color(cls, color_name):
        """Helper method to get a specific color"""
        return cls.PALETTE.get(color_name, "#000000")
    
    @classmethod
    def create_header(cls, title, subtitle=None):
        """Create a styled header with improved colors"""
        subtitle_html = f'<p style="margin: 10px 0; font-size: 1.2rem; font-weight: 300; color: white;">{subtitle}</p>' if subtitle else ''
        return f"""
        <div class="dashboard-header">
            <h1 style="margin: 0; font-size: 2.5rem; color: white; font-family: {cls.FONT_FAMILY_HEADING};">{title}</h1>
            {subtitle_html}
        </div>
        """
    
    @classmethod
    def create_info_box(cls, content, box_type="info"):
        """Create a styled info/warning/success/error box"""
        return f'<div class="{box_type}-box">{content}</div>'