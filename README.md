# Indiana Electoral Realignments (2002-2024)

An interactive data visualization mapping Indiana's political transformation across 23 years of statewide elections, revealing geographic polarization, suburban shifts, and the collapse of working-class Democratic coalitions.

![Indiana Election Map](https://img.shields.io/badge/Elections-2002--2024-blue) ![Counties](https://img.shields.io/badge/Counties-92-green) ![Contests](https://img.shields.io/badge/Contests-42-orange)

## 🗺️ Live Demo

[View the Interactive Map](https://tenjin25.github.io/INRealignmentMap/)

## 📊 Project Overview

This project visualizes Indiana's electoral realignments using a 15-level competitiveness scale, from **Tossup** to **Annihilation**, across 42 statewide contests spanning 12 election cycles. The interactive map reveals dramatic shifts:

- **Hamilton County**: R+49% (Bush 2004) → R+6% (Trump 2024) - A 43-point suburban revolt
- **Lake County**: D+35% (Obama 2008) → D+6% (Harris 2024) - A 29-point working-class erosion
- **Vigo County**: The famous bellwether that voted for Obama twice, then swung 32 points to Trump
- **Marion County**: D+2% (Kerry 2004) → D+29% (Biden 2020) - Urban transformation

## ✨ Features

### Interactive Visualization
- **Mapbox GL JS** powered county-level map with smooth zoom and pan
- **Dynamic color coding** using a 15-category competitiveness scale (75% opacity for better readability)
- **Two-party margin calculations** for consistent percentage displays
- **Responsive sidebar** with detailed county-level results and statewide aggregations
- **Contest selector** with 42 statewide races grouped by office type
- **Color-coded research findings** highlighting realignment directions (blue for leftward shifts, red for rightward shifts)

### Data Coverage
- **12 Years**: 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024
- **92 Counties**: Complete geographic coverage across all Indiana counties
- **42 Contests**: Presidential (6), Senate (7), Governor (6), Attorney General (6), Secretary of State (5), Auditor (6), Treasurer (6)
- **2-Decimal Precision**: Margins calculated to 0.01% accuracy

### Competitiveness Categories
| Category | Republican Margin | Democratic Margin | Color |
|----------|------------------|-------------------|-------|
| Tossup | <0 0.5% | < 0.50% | Gray |
| Tilt | 0.50-0.99% | 0.50-0.99% | Light Red/Blue |
| Lean | 1.00-5.49% | 1.00-5.49% | Pale Red/Blue |
| Likely | 5.50-9.99% | 5.50-9.99% | Medium Red/Blue |
| Safe | 10.00-19.99% | 10.00-19.99% | Solid Red/Blue |
| Stronghold | 20.00-29.99% | 20.00-29.99% | Deep Red/Blue |
| Dominant | 30.00-39.99% | 30.00-39.99% | Dark Red/Blue |
| Annihilation | 40%+ | 40%+ | Darkest Red/Blue |

### Research Findings
Comprehensive analysis of:
- **St. Joseph County**: Obama's 2008 breakthrough and the 2016 tossup
- **Marion County**: Indianapolis's transformation from swing county to Democratic fortress
- **Lake County**: The collapse of northwest Indiana's Democratic stronghold
- **Hamilton County**: Affluent suburban rejection of Trump-era Republicanism
- **Vigo County**: The bellwether that broke for Trump after backing Obama
- **Donut Counties**: Indianapolis suburban ring trends
- **Statewide Patterns**: Urban-rural polarization and demographic challenges

## 🛠️ Technical Stack

### Frontend
- **Mapbox GL JS**: Interactive mapping and geospatial visualization
- **JavaScript (ES6+)**: Dynamic data loading and DOM manipulation
- **HTML5/CSS3**: Responsive layout with custom styling
- **GeoJSON**: County boundary data (US Census TIGER/Line)

### Data Processing
- **Python 3.13**: Data aggregation and transformation
- **Pandas**: CSV processing and data manipulation
- **OpenElections Data**: County-level results (2002-2016)
- **Indiana Secretary of State**: AllOfficeResults format (2018-2024)

### Data Sources
- **OpenElections**: `county,office,district,candidate,party,votes` format
- **Indiana SOS 2018**: Column names with spaces ("Office Category", "Reporting County Name")
- **Indiana SOS 2020-2024**: No-space column names (OfficeCategory, ReportingCountyName)

## 📁 Project Structure

```
INRealignments/
├── index.html                    # Main application interface
├── README.md                     # This file
├── data/
│   ├── 2002/                     # OpenElections county-level CSVs
│   ├── 2004/
│   ├── ...
│   ├── 2024/
│   ├── AllOfficeResults-2018.csv # SOS precinct data
│   ├── AllOfficeResults-2020.csv
│   ├── AllOfficeResults2022.csv  # Note: no hyphen
│   ├── AllOfficeResults-2024.csv
│   ├── tl_2020_18_county20.geojson # Indiana county boundaries
│   └── indiana_election_results.json # Aggregated output
└── scripts/
    └── aggregate_statewide.py    # Data processing pipeline
```

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- A Mapbox access token (free tier available)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Tenjin25/INRealignmentMap.git
cd INRealignmentMap
```

2. **Install Python dependencies**
```bash
pip install pandas
```

3. **Configure Mapbox Token**

Edit `index.html` and replace the Mapbox access token on line ~975:
```javascript
mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN_HERE';
```

Get a free token at [mapbox.com/account/access-tokens](https://account.mapbox.com/access-tokens/)

4. **Run the data aggregation script**
```bash
python scripts/aggregate_statewide.py
```

This will process all CSV files and generate `data/indiana_election_results.json`

5. **Start a local web server**
```bash
# Python 3
python -m http.server 8000

# Or use any other local server
```

6. **Open in browser**
Navigate to `http://localhost:8000`

## 📊 Data Processing Pipeline

### Step 1: CSV Ingestion
The aggregation script handles three distinct CSV formats:

**OpenElections Format (2002-2016)**
```csv
county,office,district,candidate,party,votes
Marion,President,,Barack Obama,Democratic,171916
```

**Indiana SOS 2018 (spaces in column names)**
```csv
"Election","Office Category","Reporting County Name","Name on Ballot","Political Party","Total Votes"
```

**Indiana SOS 2020-2024 (no spaces)**
```csv
Election,OfficeCategory,ReportingCountyName,NameonBallot,PoliticalParty,TotalVotes
```

### Step 2: County Name Normalization
The script normalizes county name variations:
- "Saint Joseph" → "St. Joseph"
- "LaPort" → "Laporte"
- "DeKalb" → "Dekalb"

This ensures matching with GeoJSON county boundaries.

### Step 3: Contest Filtering
**Included offices:**
- President / Presidential Electors
- US Senate / US Senator
- Governor & Lieutenant Governor / Governor & Lt. Governor
- Attorney General
- Secretary of State
- Auditor of State
- Treasurer of State

**Excluded contests:**
- Races where one major party has <1% of two-party vote (e.g., 2006 Senate - Lugar unopposed)
- Congressional districts (gerrymandered boundaries)
- State legislature (complex redistricting)
- County/local offices

### Step 4: Margin Calculation
```python
margin = rep_votes - dem_votes
margin_pct = round((margin / two_party_total) * 100, 2)
```

### Step 5: Competitiveness Assignment
```python
if abs_margin < 0.5: category = 'Tossup'
elif abs_margin < 1: category = 'Tilt'
elif abs_margin < 5.5: category = 'Lean'
elif abs_margin < 10: category = 'Likely'
elif abs_margin < 20: category = 'Safe'
elif abs_margin < 30: category = 'Stronghold'
elif abs_margin < 40: category = 'Dominant'
else: category = 'Annihilation'
```

### Step 6: JSON Output
```json
{
  "meta": {
    "years_covered": ["2002", "2004", ..., "2024"],
    "processed_date": "2025-12-07"
  },
  "results_by_year": {
    "2024": {
      "US President & Vice President (2024)": {
        "Marion": {
          "county": "Marion",
          "dem_votes": 221719,
          "rep_votes": 124327,
          "margin_pct": -28.14,
          "competitiveness": {
            "category": "Stronghold",
            "party": "Democratic",
            "color": "#3182bd"
          }
        }
      }
    }
  }
}
```

## 🎨 Frontend Architecture

### Map Initialization
```javascript
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v11',
  center: [-86.1267, 40.2735], // Indiana centroid
  zoom: 6.5
});
```

### Dynamic Layer Updates
Contest selection triggers:
1. Parse `year|contestKey` from dropdown value
2. Load contest data from `electionData.results_by_year[year][contestKey]`
3. Build Mapbox expression matching county names (NAME20/NAMELSAD20)
4. Apply competitiveness colors using `map.setPaintProperty()`
5. Update sidebar with statewide aggregated results

### County Click Handler
```javascript
map.on('click', 'counties-fill', (e) => {
  const countyName = e.features[0].properties.NAME20;
  const countyData = currentContest.data[normalizedCountyName];
  showCountyDetails(countyData);
});
```

### Candidate Name Extraction
Since contest-level metadata varies, candidate names are derived by frequency analysis:
```javascript
const demNames = {};
const repNames = {};
Object.values(currentContest.data).forEach(county => {
  demNames[county.dem_candidate] = (demNames[county.dem_candidate] || 0) + 1;
  repNames[county.rep_candidate] = (repNames[county.rep_candidate] || 0) + 1;
});
const mostCommonDem = Object.keys(demNames).sort((a,b) => demNames[b] - demNames[a])[0];
```

## 🔍 Key Findings

### The Obama Effect (2008): Temporary Transformation

Obama's 2008 campaign achieved the seemingly impossible - turning Indiana blue for the first time since Lyndon Johnson's 1964 landslide. This wasn't just a narrow win; it represented a fundamental, if temporary, realignment across multiple county types.

**Statewide Victory**
- **Result**: Obama 1,374,039 (49.95%) vs McCain 1,345,648 (48.91%)
- **Margin**: 28,391 votes (1.03%)
- **Historic Context**: First Democratic presidential win since LBJ's 49-state sweep in 1964
- **National Significance**: Indiana became a symbol of Obama's 2008 electoral revolution

**County-Level Transformation**

*Wealthy Suburban Breakthrough*
- **Hamilton County** (Carmel/Fishers/Noblesville): Bush won by 49.39% in 2004; Obama cut it to 22.40% - a stunning 27-point swing in Indiana's wealthiest county
- **Hendricks County**: Romney-level R+48% in 2004 → R+24% in 2008 (24-point shift)
- **Johnson County**: Similar 23-point suburban swing toward Obama

*Working-Class Coalition Building*
- **Vigo County** (Terre Haute): Flipped from R+6.5% (Bush 2004) to D+16.03% (Obama 2008) - a 22.5-point swing in the famous bellwether
- **Allen County** (Fort Wayne): Cut Republican margin from R+27% to R+4% - nearly flipping Indiana's second-largest city
- **Lake County** (Gary/Hammond): Expanded from D+23% to D+35% - Obama's industrial base turnout operation

*Urban Fortress Established*
- **Marion County** (Indianapolis): D+1.94% (Kerry 2004) → D+28.61% (Obama 2008)
  - Kerry won by just 6,800 votes in 2004
  - Obama won by 107,296 votes in 2008 - a 100,000-vote swing!
  - Established Indianapolis as a reliable Democratic fortress for the next 16+ years

**Why Did Obama Win Indiana?**
1. **Record Turnout**: African American turnout in Marion and Lake counties reached historic levels
2. **Suburban College-Educated Voters**: Obama's appeal to educated professionals cracked Republican suburbs
3. **Economic Crisis**: The 2008 financial collapse and auto industry crisis devastated Indiana, turning working-class voters against Bush Republicans
4. **Ground Game**: Obama's campaign invested heavily in Indiana while McCain largely ignored it
5. **Republican Complacency**: Indiana hadn't gone Democratic in 44 years; Republicans assumed it was safe

**The Romney Rebound (2012)**

Obama narrowly lost Indiana in 2012, but county-level patterns revealed the fragility of his 2008 coalition:
- **Statewide**: Romney 1,420,543 (54.13%) vs Obama 1,152,887 (43.93%) - R+10.2%
- **Vigo County**: Went from D+16% (2008) to D+0.88% (2012) - Obama barely held the bellwether
- **Hamilton County**: Rebounded to R+34.9% - affluent voters returned to Republicans
- **Marion County**: Obama maintained D+22.62% - urban fortress held firm
- **Lake County**: D+31.34% - slight decline from 2008 peak but still strong

The 2012 results foreshadowed the coming realignment: Obama's working-class support was already eroding while urban areas remained loyal.

---

### The Trump Realignment (2016-2024): Geographic Sorting

The Trump era (2016-2024) brought unprecedented geographic polarization, with educated suburbs moving Democratic while working-class areas swung sharply Republican.

#### **Suburban Revolt: Affluent Counties Reject Trumpism**

**Hamilton County - The Canary in the Coal Mine**
- **2004**: Bush 86,624 (70.93%) vs Kerry 26,320 (21.55%) = **R+49.39% Annihilation**
- **2016**: Trump 85,695 (56.53%) vs Clinton 54,165 (35.72%) = **R+20.82% Stronghold**
- **2020**: Trump 97,877 (51.23%) vs Biden 84,590 (44.28%) = **R+6.95% Likely**
- **2024**: Trump 102,318 (51.53%) vs Harris 90,394 (45.54%) = **R+6.19% Likely**

*Analysis*: Hamilton County has undergone a 43-point swing toward Democrats since Bush's 2004 landslide. Carmel, Fishers, and Noblesville are among Indiana's most educated communities - exactly the demographic rejecting Trump nationwide. 

**Explosive Growth Factor**: Hamilton County grew from 182,740 (2000) to 347,467 (2024) - a 90% population increase making it one of the fastest-growing counties in the entire United States. This rapid suburban expansion brings younger, more diverse, college-educated transplants who are fundamentally reshaping the electorate. The influx of professionals working in Indianapolis but living in Hamilton suburbs creates a more moderate, cosmopolitan voting base than traditional Indiana Republicans.

If this trend continues, Hamilton could flip Democratic by the 2030s, threatening Republican statewide dominance.

**Other Suburban Shifts**
- **Hendricks County**: R+36.28% (2016) → R+21.87% (2024) = 14.4-point Democratic shift
- **Allen County** (Fort Wayne): R+20.56% (2016) → R+12.68% (2024) = 7.9-point Democratic shift
- **Boone County**: Another Indianapolis suburb showing similar moderation patterns

*Why Are Suburbs Moving Democratic?*
1. **Education Polarization**: College-educated voters, especially women, have shifted sharply against Trump
2. **Cultural Issues**: Suburban moderates uncomfortable with Trump's rhetoric and style
3. **Diversity**: Growing Asian and Hispanic populations in formerly white suburbs
4. **Economic Security**: Wealthy professionals less concerned about economic populism, more focused on social issues

#### **Working-Class Erosion: The Collapse of the Democratic Coalition**

**Lake County (Gary/Hammond/East Chicago) - Democratic Fortress Crumbling**
- **2008**: Obama 162,545 (64.53%) vs McCain 75,407 (29.93%) = **D+34.60% Dominant**
- **2016**: Clinton 127,929 (58.61%) vs Trump 81,084 (37.14%) = **D+21.48% Safe**
- **2020**: Biden 117,628 (54.85%) vs Trump 84,848 (39.57%) = **D+15.28% Safe**
- **2024**: Harris 109,086 (52.86%) vs Trump 97,270 (47.13%) = **D+5.73% Likely**

*Analysis*: Lake County has experienced a catastrophic 29-point swing toward Republicans since Obama's 2008 peak. This isn't just political - it reflects Gary's economic collapse, population decline (down 40% since 1960), and the disintegration of industrial unions. Harris's 6-point margin is barely "Likely Democratic" in what should be Indiana's bluest county.

**Vote Totals Tell the Story:**
- Obama 2008: 162,545 votes
- Harris 2024: 109,086 votes
- **Democratic votes declined by 53,459 (33%)** even as Republicans gained ground

**Vigo County (Terre Haute) - The Bellwether Breaks**
- **2008**: Obama 29,178 (54.59%) vs McCain 20,624 (38.57%) = **D+16.03% Safe**
- **2012**: Obama 22,931 (49.65%) vs Romney 22,525 (48.76%) = **D+0.88% Tilt** (Obama by 406 votes)
- **2016**: Trump 22,743 (55.30%) vs Clinton 16,212 (39.42%) = **R+15.86% Safe**
- **2024**: Trump 23,654 (56.63%) vs Harris 15,922 (38.12%) = **R+18.46% Safe**

*Analysis*: Vigo County voted for the winning presidential candidate in 33 of 35 elections from 1888-2020 - but broke for Trump in 2020 (Trump lost nationally) and 2024. The 32-point swing from Obama 2008 (D+16) to Trump 2024 (R+18) epitomizes the collapse of working-class Democratic support in industrial Indiana. Terre Haute, home to Indiana State University, lost thousands of manufacturing jobs and saw union influence decline dramatically.

**St. Joseph County (South Bend) - Blue Stronghold Weakening**
- **2020**: Biden 108,738 (51.47%) vs Trump 96,006 (45.45%) = **D+5.95% Likely**
- **2024**: Harris 105,104 (50.32%) vs Trump 101,474 (48.59%) = **D+1.50% Lean**

*Concern*: Even with Notre Dame and Mayor Pete Buttigieg's political base, Harris won by just 3,630 votes - down from Biden's 12,732-vote margin. If this trend continues, Democrats could lose their northern Indiana anchor.

*Why Are Working-Class Counties Moving Republican?*
1. **Deindustrialization**: Loss of manufacturing jobs weakened unions and Democratic infrastructure
2. **Cultural Issues**: Trump's appeal on immigration, guns, and "woke" culture resonates with non-college voters
3. **Economic Populism**: Trump's trade rhetoric and "forgotten man" messaging
4. **Racial Politics**: White working-class voters shifting Republican on identity issues
5. **Population Decline**: Out-migration of young, educated Democrats to cities

#### **Urban Stability: Democratic Fortresses Hold**

**Marion County (Indianapolis) - Reliable Blue Wall**
- **2016**: Clinton 235,300 (58.06%) vs Trump 144,546 (35.67%) = **D+24.04% Stronghold**
- **2020**: Biden 272,549 (60.31%) vs Trump 168,815 (37.35%) = **D+29.74% Stronghold**
- **2024**: Harris 221,719 (63.15%) vs Trump 124,327 (35.41%) = **D+28.14% Stronghold**

*Analysis*: Marion County has remained remarkably stable throughout the Trump era, delivering D+24% to D+30% margins in every election since 2012. Unlike Lake County's population decline, Indianapolis is growing, with increasing diversity and young professional in-migration. Marion produces 100,000+ vote Democratic margins that partially offset Republican dominance elsewhere.

**Other Urban/College Anchors**
- **Monroe County** (Bloomington/IU): Consistently D+35-40% - Indiana's most Democratic county
- **Tippecanoe County** (Lafayette/Purdue): Competitive due to university influence
- **Porter County** (Valparaiso/Valparaiso University): Lake Michigan suburb showing Democratic potential aided by university presence
- **Vigo County** (Terre Haute/Indiana State + Rose-Hulman): Has TWO universities (Indiana State University 10,000+ students, Rose-Hulman Institute 2,300+ students) but working-class manufacturing voters overwhelm academic liberalism - shifted from D+16% (Obama 2008) to R+18% (Trump 2024)

---

### Geographic Polarization: Two Indianas

**Urban Democratic Islands (6 of 92 counties)**
- Lake, Marion, St. Joseph (urban cores)
- Monroe (Bloomington/IU), Tippecanoe (Lafayette/Purdue) (college towns)
- Porter (Lake Michigan suburb)

These 6 counties contain ~40% of Indiana's population but are surrounded by Republican territory.

**Republican Dominance (86 of 92 counties)**
- 80+ counties deliver Republican margins
- 40+ counties exceed R+40% (Annihilation)
- 25+ counties exceed R+60% in recent elections
- Rural Indiana is now as Republican as Utah or Wyoming

**The Donut County Effect**

Marion County (Indianapolis) is surrounded by affluent Republican suburbs:
- **Hamilton County** (north): R+6% (declining)
- **Hendricks County** (west): R+22% (declining)
- **Hancock County** (east): R+40+ (stable)
- **Johnson County** (south): R+35% (declining)
- **Shelby County** (southeast): R+55+ (increasing)

This creates extreme geographic polarization visible from space on election night maps.

**Population Trends Favor Republicans**
- Rural depopulation concentrates Republicans in more counties
- Indianapolis growth doesn't offset statewide Republican lean
- Lake County decline removes Democratic votes
- Suburban growth in Hamilton/Hendricks is slow to flip blue

**The Math Problem for Democrats**

To win statewide, Democrats need:
1. Marion County margin of 120,000+ votes (achievable)
2. Lake County margin of 50,000+ votes (increasingly difficult)
3. Win or closely contest Hamilton, Tippecanoe, Monroe, St. Joseph
4. Keep rural margins below R+30% (nearly impossible now)

Current reality: Democrats can't achieve #2 and #4 simultaneously, making Indiana a safe Republican state for president (R+15-20%) despite competitive suburban trends.

## 📈 Data Quality & Limitations

### Strengths
- ✅ Complete 92-county coverage for all contests
- ✅ Official Indiana Secretary of State data (2018-2024)
- ✅ OpenElections verified data (2002-2016)
- ✅ Precinct-level aggregation for accurate county totals
- ✅ 2-decimal precision on margins

### Limitations
- ⚠️ Third-party votes grouped as "Other" (Libertarian tracked separately where available)
- ⚠️ Write-in candidates may have inconsistent naming
- ⚠️ 2006 Senate race excluded (Lugar had <1% Democratic opposition)
- ⚠️ Candidate names derived from county-level frequency (no contest-level metadata)
- ⚠️ No demographic or turnout data included

### Known Issues
- **2018 CSV Format**: Column names have spaces requiring dynamic detection
- **County Name Variants**: "Saint Joseph" vs "St. Joseph", "LaPort" vs "Laporte"
- **Contest Name Variations**: "US Senator" vs "U.S. Senate" vs "United States Senator From Indiana"

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add demographic overlays (Census data)
- [ ] Include voter registration trends
- [ ] Expand to state legislative races
- [ ] Add time-series animations
- [ ] Include turnout statistics
- [ ] Mobile-responsive improvements
- [ ] Export functionality (CSV/PNG)

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Data Sources
- **[OpenElections](http://openelections.net/)**: County-level results 2002-2016
- **[Indiana Secretary of State](https://www.in.gov/sos/elections/)**: Official election results 2018-2024
- **[US Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)**: TIGER/Line county boundaries

### Tools & Libraries
- **[Mapbox GL JS](https://www.mapbox.com/mapbox-gljs)**: Interactive mapping library
- **[Pandas](https://pandas.pydata.org/)**: Python data analysis
- **[Python](https://www.python.org/)**: Data processing pipeline

### Inspiration
- North Carolina electoral realignment analysis
- Dave Leip's Atlas of U.S. Presidential Elections
- FiveThirtyEight election cartography

## 👤 Author

**Shamar Davis**

- GitHub: [@Tenjin25](https://github.com/Tenjin25)
- Project: [INRealignmentMap](https://github.com/Tenjin25/INRealignmentMap)

## 📞 Contact & Support

Questions? Suggestions? Found a bug?

- Open an [Issue](https://github.com/Tenjin25/INRealignmentMap/issues)
- Start a [Discussion](https://github.com/Tenjin25/INRealignmentMap/discussions)
- Email: sdavis146@ivytech.edu

---

**Built with ❤️ in South Carolina for Hoosiers | Last Updated: December 7, 2025**
