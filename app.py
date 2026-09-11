# ============================================================
# Apple Inc. (AAPL) Stock Market Analysis
# Interactive EDA Dashboard
# ============================================================

import os
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AAPL Stock Analysis",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONSTANTS
# ============================================================

AAPL = "AAPL"
SP500 = "^GSPC"
TRADING_DAYS = 252

# Get the folder where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Visualization folder
IMAGE_DIR = os.path.join(BASE_DIR, "visualization")


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

        /* Main application */
        .main {
            background-color: #000000;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        /* Key findings cards */
        .insight {
            background-color: #ffffff;
            color: #111111 !important;
            border-left: 5px solid #0071e3;
            padding: 14px 18px;
            margin: 10px 0;
            border-radius: 8px;
            font-size: 16px;
            line-height: 1.5;
        }

        .insight strong {
            color: #111111 !important;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #777777;
            font-size: 13px;
            margin-top: 30px;
            margin-bottom: 20px;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA DOWNLOAD
# ============================================================

@st.cache_data(ttl=3600)
def load_data(period):
    """
    Download AAPL and S&P 500 historical data.
    """

    aapl = yf.download(
        AAPL,
        period=period,
        auto_adjust=True,
        progress=False,
    )

    sp500 = yf.download(
        SP500,
        period=period,
        auto_adjust=True,
        progress=False,
    )

    return clean_data(aapl), clean_data(sp500)


# ============================================================
# DATA CLEANING
# ============================================================

def clean_data(df):
    """
    Clean yfinance downloaded data.
    """

    if df.empty:
        return df

    df = df.copy()

    # Handle MultiIndex columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # Remove rows where Close is missing
    if "Close" in df.columns:
        df = df.dropna(subset=["Close"])

    return df


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(df):
    """
    Calculate key stock performance metrics.
    """

    close = df["Close"]

    returns = close.pct_change().dropna()

    # Number of years
    years = (
        (close.index[-1] - close.index[0]).days
        / 365.25
    )

    # Total return
    total_return = (
        (close.iloc[-1] / close.iloc[0] - 1)
        * 100
    )

    # Annualized return
    if years > 0:

        annual_return = (
            (close.iloc[-1] / close.iloc[0])
            ** (1 / years)
            - 1
        ) * 100

    else:

        annual_return = np.nan

    # Annualized volatility
    volatility = (
        returns.std()
        * np.sqrt(TRADING_DAYS)
        * 100
    )

    # Sharpe ratio
    # Risk-free rate assumed to be 0%
    if returns.std() != 0:

        sharpe = (
            returns.mean()
            / returns.std()
            * np.sqrt(TRADING_DAYS)
        )

    else:

        sharpe = np.nan

    # Drawdown
    rolling_max = close.cummax()

    drawdown = (
        close / rolling_max
        - 1
    )

    max_drawdown = drawdown.min() * 100

    return {
        "price": close.iloc[-1],
        "daily_change": returns.iloc[-1] * 100,
        "total_return": total_return,
        "annual_return": annual_return,
        "volatility": volatility,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "best_day": returns.max() * 100,
        "worst_day": returns.min() * 100,
        "positive_days": (returns > 0).mean() * 100,
        "negative_days": (returns < 0).mean() * 100,
        "avg_volume": df["Volume"].mean(),
    }


# ============================================================
# PRICE CHART
# ============================================================

def price_chart(
    df,
    ma50=True,
    ma200=True,
):

    data = df.copy()

    # Moving averages
    data["MA50"] = (
        data["Close"]
        .rolling(50)
        .mean()
    )

    data["MA200"] = (
        data["Close"]
        .rolling(200)
        .mean()
    )

    fig = go.Figure()

    # AAPL price
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            name="AAPL",
            line=dict(
                color="#0071e3",
                width=2,
            ),
        )
    )

    # 50-day MA
    if ma50:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA50"],
                name="50-Day MA",
                line=dict(
                    color="#ff9500",
                    width=1.5,
                ),
            )
        )

    # 200-day MA
    if ma200:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA200"],
                name="200-Day MA",
                line=dict(
                    color="#ff3b30",
                    width=1.5,
                ),
            )
        )

    fig.update_layout(
        title="AAPL Price Trend",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_white",
        hovermode="x unified",
        height=500,
    )

    return fig


# ============================================================
# CANDLESTICK CHART
# ============================================================

def candlestick_chart(df):

    fig = go.Figure(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            increasing_line_color="#34c759",
            decreasing_line_color="#ff3b30",
            name="AAPL",
        )
    )

    fig.update_layout(
        title="AAPL Candlestick Chart",
        template="plotly_white",
        height=500,
        xaxis_rangeslider_visible=False,
    )

    return fig


# ============================================================
# RETURNS CHART
# ============================================================

def returns_chart(df):

    returns = (
        df["Close"]
        .pct_change()
        * 100
    )

    colors = np.where(
        returns >= 0,
        "#34c759",
        "#ff3b30",
    )

    fig = go.Figure(
        go.Bar(
            x=df.index,
            y=returns,
            marker_color=colors,
            name="Daily Return",
        )
    )

    fig.update_layout(
        title="Daily Returns",
        xaxis_title="Date",
        yaxis_title="Return (%)",
        template="plotly_white",
        height=420,
    )

    return fig


# ============================================================
# DISTRIBUTION CHART
# ============================================================

def distribution_chart(df):

    returns = (
        df["Close"]
        .pct_change()
        .dropna()
        * 100
    )

    fig = go.Figure(
        go.Histogram(
            x=returns,
            nbinsx=70,
            marker_color="#0071e3",
        )
    )

    fig.update_layout(
        title="Distribution of Daily Returns",
        xaxis_title="Daily Return (%)",
        yaxis_title="Frequency",
        template="plotly_white",
        height=420,
    )

    return fig


# ============================================================
# DRAWDOWN CHART
# ============================================================

def drawdown_chart(df):

    close = df["Close"]

    drawdown = (
        close / close.cummax()
        - 1
    ) * 100

    fig = go.Figure(
        go.Scatter(
            x=df.index,
            y=drawdown,
            mode="lines",
            fill="tozeroy",
            line=dict(
                color="#ff3b30"
            ),
            fillcolor="rgba(255,59,48,0.20)",
            name="Drawdown",
        )
    )

    fig.update_layout(
        title="AAPL Drawdown",
        xaxis_title="Date",
        yaxis_title="Drawdown (%)",
        template="plotly_white",
        height=420,
    )

    return fig


# ============================================================
# VOLUME CHART
# ============================================================

def volume_chart(df):

    colors = np.where(
        df["Close"] >= df["Open"],
        "#34c759",
        "#ff3b30",
    )

    fig = go.Figure(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            marker_color=colors,
            name="Volume",
        )
    )

    fig.update_layout(
        title="Trading Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_white",
        height=420,
    )

    return fig


# ============================================================
# BENCHMARK CHART
# ============================================================

def benchmark_chart(
    aapl,
    sp500,
):

    data = pd.concat(
        [
            aapl["Close"].rename("AAPL"),
            sp500["Close"].rename("S&P 500"),
        ],
        axis=1,
    ).dropna()

    normalized = (
        data
        / data.iloc[0]
        * 100
    )

    fig = go.Figure()

    # AAPL
    fig.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized["AAPL"],
            name="AAPL",
            line=dict(
                color="#0071e3",
                width=2.5,
            ),
        )
    )

    # S&P 500
    fig.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized["S&P 500"],
            name="S&P 500",
            line=dict(
                color="#ff9500",
                width=2.5,
            ),
        )
    )

    fig.update_layout(
        title="AAPL vs S&P 500",
        xaxis_title="Date",
        yaxis_title="Growth of $100",
        template="plotly_white",
        hovermode="x unified",
        height=500,
    )

    return fig


# ============================================================
# MONTHLY PERFORMANCE
# ============================================================

def monthly_returns(df):

    monthly = (
        df["Close"]
        .resample("ME")
        .last()
        .pct_change()
        * 100
    )

    result = monthly.to_frame(
        "Return"
    )

    result["Year"] = (
        result.index.year
    )

    result["Month"] = (
        result.index.month
    )

    return result


# ============================================================
# IMAGE DISPLAY
# ============================================================

def display_project_image(
    filename,
    caption,
):

    path = os.path.join(
        IMAGE_DIR,
        filename,
    )

    if os.path.isfile(path):

        st.image(
            path,
            caption=caption,
            use_container_width=True,
        )

    else:

        st.error(
            f"❌ Image not found: {path}"
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🍎 AAPL Analysis"
)


periods = {
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "10 Years": "10y",
    "Maximum": "max",
}


selected_period = st.sidebar.selectbox(
    "Historical Period",
    list(periods.keys()),
    index=2,
)


show_ma50 = st.sidebar.checkbox(
    "50-Day Moving Average",
    True,
)


show_ma200 = st.sidebar.checkbox(
    "200-Day Moving Average",
    True,
)


st.sidebar.divider()


st.sidebar.info(
    """
    **Data Source**

    Yahoo Finance through yfinance.

    Historical data is used for
    educational and exploratory
    analysis only.
    """
)


# ============================================================
# LOAD DATA
# ============================================================

with st.spinner(
    "Loading market data..."
):

    aapl, sp500 = load_data(
        periods[selected_period]
    )


# ============================================================
# CHECK DATA
# ============================================================

if aapl.empty or sp500.empty:

    st.error(
        "Unable to download market data. "
        "Please try again later."
    )

    st.stop()


# ============================================================
# CALCULATE METRICS
# ============================================================

metrics = calculate_metrics(
    aapl
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🍎 Apple Inc. (AAPL) Stock Market Analysis"
)


st.markdown(
    """
    **Exploratory Data Analysis Dashboard**

    Analyze Apple's historical price movements, returns,
    volatility, trading volume, drawdowns, moving averages,
    and performance relative to the S&P 500.
    """
)


st.caption(
    f"{aapl.index[0].strftime('%d %b %Y')} → "
    f"{aapl.index[-1].strftime('%d %b %Y')}"
)


# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================

st.subheader(
    "📊 Key Performance Indicators"
)


c1, c2, c3, c4, c5 = st.columns(5)


c1.metric(
    "Latest Price",
    f"${metrics['price']:,.2f}",
)


c2.metric(
    "Total Return",
    f"{metrics['total_return']:+.2f}%",
)


c3.metric(
    "Annualized Return",
    f"{metrics['annual_return']:+.2f}%",
)


c4.metric(
    "Volatility",
    f"{metrics['volatility']:.2f}%",
)


c5.metric(
    "Max Drawdown",
    f"{metrics['max_drawdown']:.2f}%",
)


# ============================================================
# TABS
# ============================================================

overview, price, returns, risk, comparison, data = st.tabs(
    [
        "📊 Overview",
        "📈 Price",
        "💰 Returns",
        "⚠️ Risk",
        "🆚 Benchmark",
        "🗃️ Data",
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with overview:

    st.subheader(
        "Project Overview"
    )


    # --------------------------------------------------------
    # INTRODUCTION
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [1, 2]
    )


    with col1:

        display_project_image(
            "AAPL_adjusted_closing_price.png",
            "AAPL Adjusted Closing Price",
        )


    with col2:

        st.markdown(
            """
            ### What this analysis studies

            This project uses historical AAPL market data to
            perform exploratory data analysis of Apple Inc.

            The dashboard investigates:

            - Stock price trends
            - Daily returns
            - Return distribution
            - Volatility
            - Trading volume
            - Drawdowns
            - Moving averages
            - Monthly performance
            - Annual performance
            - AAPL vs S&P 500 performance
            - AAPL and S&P 500 return correlation
            - Volume vs daily returns
            """
        )


    st.divider()


    # --------------------------------------------------------
    # KEY FINDINGS
    # --------------------------------------------------------

    st.subheader(
        "🔎 Key Findings"
    )


    findings = [

        f"AAPL generated a total return of "
        f"{metrics['total_return']:+.2f}% "
        f"over the selected period.",

        f"The annualized return was "
        f"{metrics['annual_return']:+.2f}%.",

        f"AAPL's annualized volatility was "
        f"{metrics['volatility']:.2f}%, "
        f"indicating the level of price fluctuation.",

        f"The maximum observed drawdown was "
        f"{metrics['max_drawdown']:.2f}%.",

        f"The best trading day produced a return of "
        f"{metrics['best_day']:+.2f}%.",

        f"The worst trading day produced a return of "
        f"{metrics['worst_day']:+.2f}%.",

        f"{metrics['positive_days']:.2f}% "
        f"of trading days had positive returns.",

        f"{metrics['negative_days']:.2f}% "
        f"of trading days had negative returns.",
    ]


    for finding in findings:

        st.markdown(
            f"""
            <div class="insight">
                💡 {finding}
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.divider()


    # --------------------------------------------------------
    # PROJECT VISUALIZATIONS
    # --------------------------------------------------------

    st.subheader(
        "📊 Project Visualizations"
    )


    # ========================================================
    # ROW 1
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        display_project_image(
            "AAPL_price_moving_averages.png",
            "AAPL Price and Moving Averages",
        )


    with col2:

        display_project_image(
            "AAPL_daily_returns_distribution.png",
            "AAPL Daily Returns Distribution",
        )


    # ========================================================
    # ROW 2
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        display_project_image(
            "AAPL_trading_volume.png",
            "AAPL Trading Volume",
        )


    with col2:

        display_project_image(
            "AAPL_historical_drawdown.png",
            "AAPL Historical Drawdown",
        )


    # ========================================================
    # ROW 3
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        display_project_image(
            "AAPL_vs_SP500_cumulative_performance.png",
            "AAPL vs S&P 500 Cumulative Performance",
        )


    with col2:

        display_project_image(
            "AAPL_monthly_returns_heatmap.png",
            "AAPL Monthly Returns Heatmap",
        )


    # ========================================================
    # ROW 4
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        display_project_image(
            "AAPL_annual_returns.png",
            "AAPL Annual Returns",
        )


    with col2:

        display_project_image(
            "AAPL_30day_rolling_annualized_volatility.png",
            "AAPL 30-Day Rolling Annualized Volatility",
        )


    # ========================================================
    # ROW 5
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        display_project_image(
            "AAPL_SP500_return_correlation.png",
            "AAPL vs S&P 500 Return Correlation",
        )


    with col2:

        display_project_image(
            "AAPL_volume_vs_daily_returns.png",
            "AAPL Volume vs Daily Returns",
        )


# ============================================================
# PRICE ANALYSIS
# ============================================================

with price:

    st.subheader(
        "📈 Historical Price Analysis"
    )


    st.plotly_chart(
        price_chart(
            aapl,
            show_ma50,
            show_ma200,
        ),
        use_container_width=True,
    )


    st.markdown(
        """
        **Moving Average Interpretation**

        The 50-day moving average helps identify short-term
        trends, while the 200-day moving average provides a
        longer-term trend indicator.
        """
    )


    st.subheader(
        "Candlestick Analysis"
    )


    st.plotly_chart(
        candlestick_chart(aapl),
        use_container_width=True,
    )


# ============================================================
# RETURNS
# ============================================================

with returns:

    st.subheader(
        "💰 Return Analysis"
    )


    st.plotly_chart(
        returns_chart(aapl),
        use_container_width=True,
    )


    col1, col2 = st.columns(2)


    with col1:

        st.plotly_chart(
            distribution_chart(aapl),
            use_container_width=True,
        )


    with col2:

        returns_data = (
            aapl["Close"]
            .pct_change()
            .dropna()
            * 100
        )


        stats = pd.DataFrame(
            {
                "Statistic": [
                    "Mean",
                    "Median",
                    "Std. Deviation",
                    "Minimum",
                    "Maximum",
                    "25th Percentile",
                    "75th Percentile",
                ],

                "Return (%)": [
                    returns_data.mean(),
                    returns_data.median(),
                    returns_data.std(),
                    returns_data.min(),
                    returns_data.max(),
                    returns_data.quantile(0.25),
                    returns_data.quantile(0.75),
                ],
            }
        )


        st.subheader(
            "Return Statistics"
        )


        st.dataframe(
            stats.style.format(
                {
                    "Return (%)": "{:.4f}%"
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


    st.divider()


    # --------------------------------------------------------
    # MONTHLY PERFORMANCE
    # --------------------------------------------------------

    st.subheader(
        "📅 Monthly Performance"
    )


    monthly = monthly_returns(
        aapl
    )


    pivot = monthly.pivot(
        index="Year",
        columns="Month",
        values="Return",
    )


    # Convert month numbers to names
    pivot.columns = [

        pd.Timestamp(
            year=2000,
            month=int(month),
            day=1,
        ).strftime("%b")

        for month in pivot.columns

    ]


    fig = go.Figure(

        go.Heatmap(

            z=pivot.values,

            x=pivot.columns,

            y=pivot.index,

            colorscale=[
                [0, "#ff3b30"],
                [0.5, "#ffffff"],
                [1, "#34c759"],
            ],

            zmid=0,

            text=np.round(
                pivot.values,
                2,
            ),

            texttemplate="%{text}%",

            colorbar_title="Return %",
        )
    )


    fig.update_layout(
        title="Monthly Returns Heatmap",
        template="plotly_white",
        height=500,
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# RISK
# ============================================================

with risk:

    st.subheader(
        "⚠️ Risk Analysis"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Annualized Volatility",
        f"{metrics['volatility']:.2f}%",
    )


    c2.metric(
        "Sharpe Ratio",
        f"{metrics['sharpe']:.2f}",
    )


    c3.metric(
        "Maximum Drawdown",
        f"{metrics['max_drawdown']:.2f}%",
    )


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.plotly_chart(
            drawdown_chart(aapl),
            use_container_width=True,
        )


    with col2:

        st.plotly_chart(
            volume_chart(aapl),
            use_container_width=True,
        )


    st.subheader(
        "Trading Activity"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Average Volume",
        f"{metrics['avg_volume']:,.0f}",
    )


    c2.metric(
        "Positive Days",
        f"{metrics['positive_days']:.2f}%",
    )


    c3.metric(
        "Negative Days",
        f"{metrics['negative_days']:.2f}%",
    )


# ============================================================
# BENCHMARK COMPARISON
# ============================================================

with comparison:

    st.subheader(
        "🆚 AAPL vs S&P 500"
    )


    comparison_data = pd.concat(
        [
            aapl["Close"].rename("AAPL"),
            sp500["Close"].rename("S&P 500"),
        ],
        axis=1,
    ).dropna()


    # AAPL return
    aapl_return = (

        comparison_data["AAPL"].iloc[-1]
        /
        comparison_data["AAPL"].iloc[0]
        - 1

    ) * 100


    # S&P 500 return
    sp500_return = (

        comparison_data["S&P 500"].iloc[-1]
        /
        comparison_data["S&P 500"].iloc[0]
        - 1

    ) * 100


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "AAPL Return",
        f"{aapl_return:+.2f}%",
    )


    c2.metric(
        "S&P 500 Return",
        f"{sp500_return:+.2f}%",
    )


    c3.metric(
        "Difference",
        f"{aapl_return - sp500_return:+.2f}%",
    )


    st.plotly_chart(
        benchmark_chart(
            aapl,
            sp500,
        ),
        use_container_width=True,
    )


    st.info(
        """
        Both assets are normalized to 100 at the beginning
        of the selected period. This allows their relative
        performance to be compared despite different starting prices.
        """
    )


# ============================================================
# DATA
# ============================================================

with data:

    st.subheader(
        "🗃️ Historical AAPL Data"
    )


    display_data = aapl.copy()


    display_data[
        "Daily Return (%)"
    ] = (

        display_data["Close"]
        .pct_change()
        * 100

    )


    st.dataframe(
        display_data.sort_index(
            ascending=False
        ),
        use_container_width=True,
        height=600,
    )


    # CSV download
    csv = (
        display_data
        .to_csv()
        .encode("utf-8")
    )


    st.download_button(
        "⬇️ Download CSV",

        data=csv,

        file_name="AAPL_stock_analysis.csv",

        mime="text/csv",
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.markdown(
    """
    <div class="footer">

        Apple Inc. (AAPL) Stock Market Analysis
        |
        Python • Streamlit • Pandas • NumPy • Plotly • yfinance

        <br><br>

        Educational and analytical purposes only.
        Historical performance does not guarantee future results.

    </div>
    """,
    unsafe_allow_html=True,
)
