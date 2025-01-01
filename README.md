
# Web Server Log Analysis Project

## Overview
This project focuses on analyzing over 35 million HTTP requests from a Poland-based e-commerce platform to uncover patterns in user behavior and system performance. By leveraging Python and visualizing data through a Streamlit-based UI, the project converts raw server logs into actionable insights.

## Dataset Details
- **Source**: Web server logs from a Poland-based e-commerce site.
- **Period**: December 1, 2019, to May 31, 2020 (183 days).
- **Size**: 35,157,691 HTTP requests stored in CSV format (~9.1 GB raw, ~10.7 GB processed).
- **Features**:
  - **IpId**: Anonymized IP with country identifier.
  - **UserId**: Differentiates between regular and admin users.
  - **TimeStamp**: Converted from Windows FileTime to a datetime format.
  - **HttpMethod**: Types of HTTP requests (GET, POST, etc.).
  - **Uri**: Partially redacted resource identifiers.
  - **HttpVersion**, **ResponseCode**, **Bytes**, **Referrer**, **UserAgent**.

## Preprocessing
1. **Datetime Conversion**: Timestamps transformed into human-readable datetime format.
2. **Feature Engineering**:
   - Extracted `CountryCode` from `IpId`.
   - Parsed `UserAgent` to extract `Browser`, `OS`, and `Device_Type`.
   - Categorized `Uri` into `URI_Type` and `Referrer` into `Referrer_Type`.
3. **Data Cleaning**: Removed irrelevant `UserId` column, handled missing values.
4. **Storage**: Final dataset saved in CSV format with enriched features.

## Analysis Performed
### Traffic Analysis
- Examined distribution of HTTP methods (GET, POST).
- Analyzed response codes for user experience and security insights.
- Identified key traffic metrics: 519.92 GB total data transfer, HTTP 200 as the most common response.

### Temporal Analysis
- Identified peak activity hours (18:00–20:00), with a notable spike at 20:00 (14,402 requests).

### Geographical Analysis
- Major traffic from Poland (PL), followed by the US, Netherlands, and Germany.
- Logarithmic scaling used to highlight disparities between major and minor contributors.

### User Agent Analysis
- Chrome and Firefox were the dominant browsers.
- Significant traffic from Windows (53%) and Linux (40%), indicating a tech-savvy user base.

### Session Analysis
- Sessions defined as periods of activity with thresholds (2–120 minutes, 30-minute inactivity cutoff).
- Explored engagement patterns with URI types, referrers, and geographic data.

## Visualization
- Graphs and charts illustrate trends in traffic, user agents, referrers, and more.
- Key insights are displayed in a user-friendly Streamlit interface.

## How to Use This Repository
1. Clone the repository:
   ```bash
   git clone https://github.com/project506/WebServerLogAnalysis.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Dependencies
- `pandas`, `numpy`, `matplotlib`, `seaborn`, `streamlit`, and others.

## Results
- Deep insights into user behavior, session dynamics, and system performance.
- Actionable recommendations for website optimization, security, and marketing strategies.

## License
This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.


