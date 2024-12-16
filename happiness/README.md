**Narrative: Understanding Global Happiness Through Data**

The world is a complex tapestry of experiences, emotions, and aspirations, woven together by the threads of culture, economy, and societal values. The dataset we have, comprising 2,363 entries and 11 distinct columns, provides a fascinating glimpse into the factors influencing happiness across various nations. From the 'Life Ladder' to 'Log GDP per capita', this data reveals the intricate dynamics of what makes people feel fulfilled and content in their lives.

### **The Happiness Index: A Closer Look**

At the core of this analysis lies the 'Life Ladder' metric, which serves as a proxy for subjective well-being. With an average score of 5.48, it's evident that while many are finding joy in their lives, there remains significant room for improvement. The scores range from a low of 1.28 to a high of 8.02, indicating a wide disparity in happiness levels globally. Notably, the nations with the highest happiness ratings, such as Norway and Denmark, showcase a remarkable combination of strong social support systems, high life expectancy, and robust economies.

### **Economic Factors: The Log GDP Connection**

Our analysis shows a strong correlation between 'Log GDP per capita' and happiness. The average GDP per capita in the dataset is about 9.40, with a maximum value reaching 11.68. This suggests that wealthier nations generally report higher life satisfaction, reinforcing the idea that economic stability plays a crucial role in enhancing individual happiness. However, it's essential to remember that wealth alone does not guarantee happiness; the interdependence of social support, freedom, and individual agency cannot be overlooked.

### **The Role of Social Support and Freedom**

The dataset highlights the significance of social support, with an average score of 0.81. Nations that invest in community and social networks tend to foster environments where individuals feel valued and connected. Similarly, the 'Freedom to make life choices' averages 0.75, emphasizing the importance of autonomy in achieving happiness. Countries that allow their citizens the freedom to pursue their desires and goals often see higher levels of contentment.

### **Corruption, Generosity, and Affect: Beyond the Surface**

Interestingly, the perceptions of corruption average about 0.74, suggesting that transparency and trust in governance significantly impact happiness. Countries that are perceived as more corrupt tend to have lower happiness scores, revealing the detrimental effects of distrust on societal well-being.

Generosity, however, presents a more complex picture. With an average score near zero and a maximum of 0.70, it indicates that while altruism can enhance individual happiness, it is not universally felt or recognized across nations. The concept of positive and negative affect—averaging 0.65 and 0.27 respectively—provides further insight into the emotional landscape of different countries, showing that while many experience joy, a considerable portion also grapples with negativity.

### **Challenges in the Data: Missing Values and Outliers**

As we dive deeper, we encounter some challenges within our dataset. Missing values abound, particularly in 'Generosity' (81 missing entries) and 'Perceptions of corruption' (125 missing entries). This data gap highlights the need for caution when interpreting findings and suggests that certain countries may be underrepresented in our analysis.

Outliers, such as Afghanistan, present stark contrasts to the global averages, with consistently low happiness scores and economic indicators. This serves as a reminder that not every nation enjoys the benefits of wealth and social structure, underscoring the urgency for targeted interventions in areas grappling with conflict and instability.

### **Conclusion: A Path Forward**

In conclusion, the happiness dataset reveals a rich narrative about the state of global well-being. It highlights the interconnectedness of economic prosperity, social support, freedom, and the perceptions of corruption in shaping happiness levels. 

As we reflect on these findings, we must consider the implications for policymakers and global leaders. Addressing economic disparities, enhancing social networks, and promoting transparency could pave the way for a more joyful world. After all, the journey to happiness is not just an individual pursuit but a collective responsibility. By understanding the data, we can foster environments that nurture well-being for all, leaving no one behind on this ladder of life.
### Exploratory Data Analysis
### CSV File Name: happiness.csv
### Dataset Overview
- **Shape:** 2363 rows and 11 columns
### Columns and Data Types:
```plaintext
Country name                         object
year                                  int64
Life Ladder                         float64
Log GDP per capita                  float64
Social support                      float64
Healthy life expectancy at birth    float64
Freedom to make life choices        float64
Generosity                          float64
Perceptions of corruption           float64
Positive affect                     float64
Negative affect                     float64
```
### Sample Rows:
```plaintext
              Country name  year  Life Ladder  Log GDP per capita  Social support  Healthy life expectancy at birth  Freedom to make life choices  Generosity  Perceptions of corruption  Positive affect  Negative affect
1589                Norway  2018        7.444              11.077           0.966                            71.350                         0.960       0.086                      0.268            0.786            0.212
1989                Sweden  2008        7.516              10.778           0.923                            71.120                         0.912       0.120                      0.314            0.763            0.134
2151               Türkiye  2020        4.862              10.257           0.857                            68.575                         0.510      -0.119                      0.774            0.332            0.440
2193  United Arab Emirates  2010        7.097              10.909           0.912                            65.100                         0.878       0.051                      0.355            0.701            0.233
709                  Gabon  2021        5.075               9.533           0.754                            58.250                         0.699      -0.207                      0.766            0.620            0.362
556                Denmark  2023        7.504              10.996           0.916                            71.500                         0.923       0.089                      0.184            0.757            0.229
1671           Philippines  2011        4.994               8.699           0.789                            61.660                         0.883       0.068                      0.783            0.808            0.358
2202  United Arab Emirates  2019        6.711              11.181           0.862                            66.000                         0.911       0.118                        NaN            0.730            0.284
2314                 Yemen  2007        4.477               8.212           0.825                            58.720                         0.673       0.006                        NaN            0.524            0.379
1502           New Zealand  2010        7.224              10.534           0.976                            69.800                         0.918       0.247                      0.321            0.783            0.235
386                   Chad  2022        4.397               7.253           0.720                            53.125                         0.679       0.218                      0.805            0.588            0.499
2285             Venezuela  2013        6.553               9.802           0.896                            65.180                         0.642      -0.230                      0.837            0.812            0.238
311                Burundi  2014        2.905               6.723           0.565                            53.380                         0.431      -0.059                      0.808            0.622            0.251
1904          South Africa  2020        4.947               9.458           0.891                            56.725                         0.757      -0.030                      0.912            0.761            0.294
537                Czechia  2022        6.695              10.637           0.944                            69.175                         0.908       0.093                      0.831            0.743            0.246
2067              Tanzania  2014        3.483               7.717           0.789                            56.040                         0.654       0.107                      0.878            0.693            0.241
148             Bangladesh  2012        4.724               8.231           0.582                            62.240                         0.668      -0.051                      0.765            0.537            0.183
1025               Jamaica  2020        5.425               9.128           0.870                            66.600                         0.865      -0.152                      0.836            0.712            0.266
844               Honduras  2022        5.932               8.650           0.729                            64.275                         0.851       0.078                      0.834            0.775            0.289
1334            Mauritania  2014        4.483               8.521           0.853                            58.600                         0.468      -0.060                      0.589            0.743            0.163
1150                  Laos  2008        5.044               8.351           0.807                            56.640                         0.886       0.412                      0.637            0.728            0.202
781                 Greece  2017        5.148              10.261           0.753                            70.650                         0.438      -0.295                      0.872            0.516            0.333
1695                Poland  2018        6.111              10.365           0.863                            68.525                         0.870      -0.260                      0.720            0.622            0.176
925                   Iran  2008        5.129               9.584           0.633                            64.720                         0.601       0.040                      0.868            0.541            0.345
1505           New Zealand  2013        7.280              10.585           0.958                            69.860                         0.944       0.230                      0.312            0.778            0.151
2279             Venezuela  2006        6.525               9.467           0.946                            65.460                         0.798      -0.037                      0.646            0.837            0.178
1271                Malawi  2016        3.476               7.270           0.524                            55.450                         0.810       0.037                      0.824            0.584            0.325
2252               Uruguay  2015        6.628              10.032           0.891                            67.500                         0.917      -0.045                      0.673            0.812            0.300
1436            Mozambique  2015        4.550               7.148           0.666                            48.600                         0.813       0.083                      0.632            0.560            0.340
401                  Chile  2019        5.942              10.119           0.869                            70.000                         0.659      -0.110                      0.860            0.741            0.337
111                Austria  2021        7.080              10.899           0.863                            71.150                         0.795       0.158                      0.501            0.722            0.259
1936                 Spain  2012        6.291              10.485           0.937                            71.240                         0.755      -0.065                      0.844            0.644            0.366
965                Ireland  2018        6.962              11.334           0.938                            71.000                         0.861       0.138                      0.362            0.754            0.213
921              Indonesia  2022        5.585               9.426           0.834                            63.175                         0.903       0.516                      0.862            0.818            0.269
651               Eswatini  2018        4.212               9.029           0.779                            49.300                         0.710      -0.182                      0.692            0.739            0.252
2353              Zimbabwe  2014        4.184               7.748           0.766                            50.000                         0.642      -0.062                      0.820            0.661            0.239
1960             Sri Lanka  2019        4.213               9.521           0.815                            67.000                         0.824       0.043                      0.863            0.753            0.315
480             Costa Rica  2013        7.158               9.801           0.902                            69.680                         0.898       0.009                      0.813            0.809            0.278
132                Bahrain  2011        4.824              10.749           0.908                            65.240                         0.870      -0.061                      0.583            0.506            0.514
251               Botswana  2014        4.031               9.593           0.859                            52.360                         0.791      -0.099                      0.743            0.626            0.245
105                Austria  2015        7.076              10.876           0.928                            70.400                         0.900       0.093                      0.557            0.748            0.164
4              Afghanistan  2012        3.783               7.661           0.521                            51.700                         0.531       0.234                      0.776            0.614            0.268
919              Indonesia  2020        4.828               9.351           0.751                            62.925                         0.853       0.529                      0.914            0.742            0.351
2262            Uzbekistan  2008        5.311               8.402           0.894                            61.820                         0.831      -0.033                        NaN            0.647            0.187
739                Germany  2010        6.725              10.758           0.939                            70.000                         0.843       0.089                      0.688            0.698            0.182
258               Botswana  2023        3.332               9.673           0.701                            55.000                         0.741      -0.264                      0.814            0.657            0.247
683                 France  2008        7.008              10.669           0.935                            71.000                         0.833      -0.037                      0.669            0.702            0.281
1005                 Italy  2022        6.258              10.687           0.869                            72.125                         0.711       0.026                      0.819            0.624            0.298
1963             Sri Lanka  2022        3.985               9.409           0.825                            67.300                         0.740       0.038                      0.900            0.715            0.321
2165                Uganda  2016        4.233               7.667           0.754                            56.775                         0.739       0.125                      0.811            0.665            0.410
```
### Basic Statistics
```plaintext
       Country name         year  Life Ladder  Log GDP per capita  Social support  Healthy life expectancy at birth  Freedom to make life choices   Generosity  Perceptions of corruption  Positive affect  Negative affect
count          2363  2363.000000  2363.000000         2335.000000     2350.000000                       2300.000000                   2327.000000  2282.000000                2238.000000      2339.000000      2347.000000
unique          165          NaN          NaN                 NaN             NaN                               NaN                           NaN          NaN                        NaN              NaN              NaN
top         Lebanon          NaN          NaN                 NaN             NaN                               NaN                           NaN          NaN                        NaN              NaN              NaN
freq             18          NaN          NaN                 NaN             NaN                               NaN                           NaN          NaN                        NaN              NaN              NaN
mean            NaN  2014.763860     5.483566            9.399671        0.809369                         63.401828                      0.750282     0.000098                   0.743971         0.651882         0.273151
std             NaN     5.059436     1.125522            1.152069        0.121212                          6.842644                      0.139357     0.161388                   0.184865         0.106240         0.087131
min             NaN  2005.000000     1.281000            5.527000        0.228000                          6.720000                      0.228000    -0.340000                   0.035000         0.179000         0.083000
25%             NaN  2011.000000     4.647000            8.506500        0.744000                         59.195000                      0.661000    -0.112000                   0.687000         0.572000         0.209000
50%             NaN  2015.000000     5.449000            9.503000        0.834500                         65.100000                      0.771000    -0.022000                   0.798500         0.663000         0.262000
75%             NaN  2019.000000     6.323500           10.392500        0.904000                         68.552500                      0.862000     0.093750                   0.867750         0.737000         0.326000
max             NaN  2023.000000     8.019000           11.676000        0.987000                         74.600000                      0.985000     0.700000                   0.983000         0.884000         0.705000
```
### Missing Values
```plaintext
Log GDP per capita                   28
Social support                       13
Healthy life expectancy at birth     63
Freedom to make life choices         36
Generosity                           81
Perceptions of corruption           125
Positive affect                      24
Negative affect                      16
```
## Correlation Matrix
```plaintext
                                      year  Life Ladder  Log GDP per capita  Social support  Healthy life expectancy at birth  Freedom to make life choices  Generosity  Perceptions of corruption  Positive affect  Negative affect
year                              1.000000     0.046846            0.080104       -0.043074                          0.168026                      0.232974    0.030864                  -0.082136         0.013052         0.207642
Life Ladder                       0.046846     1.000000            0.783556        0.722738                          0.714927                      0.538210    0.177398                  -0.430485         0.515283        -0.352412
Log GDP per capita                0.080104     0.783556            1.000000        0.685329                          0.819326                      0.364816   -0.000766                  -0.353893         0.230868        -0.260689
Social support                   -0.043074     0.722738            0.685329        1.000000                          0.597787                      0.404131    0.065240                  -0.221410         0.424524        -0.454878
Healthy life expectancy at birth  0.168026     0.714927            0.819326        0.597787                          1.000000                      0.375745    0.015168                  -0.303130         0.217982        -0.150330
Freedom to make life choices      0.232974     0.538210            0.364816        0.404131                          0.375745                      1.000000    0.321396                  -0.466023         0.578398        -0.278959
Generosity                        0.030864     0.177398           -0.000766        0.065240                          0.015168                      0.321396    1.000000                  -0.270004         0.300608        -0.071975
Perceptions of corruption        -0.082136    -0.430485           -0.353893       -0.221410                         -0.303130                     -0.466023   -0.270004                   1.000000        -0.274208         0.265555
Positive affect                   0.013052     0.515283            0.230868        0.424524                          0.217982                      0.578398    0.300608                  -0.274208         1.000000        -0.334451
Negative affect                   0.207642    -0.352412           -0.260689       -0.454878                         -0.150330                     -0.278959   -0.071975                   0.265555        -0.334451         1.000000
```
![Correlation Matrix](correlation_matrix.png)
## Outlier Detection
- **year:** 0 outliers
- **Life Ladder:** 2 outliers
- **Log GDP per capita:** 1 outliers
- **Social support:** 48 outliers
- **Healthy life expectancy at birth:** 20 outliers
- **Freedom to make life choices:** 16 outliers
- **Generosity:** 39 outliers
- **Perceptions of corruption:** 194 outliers
- **Positive affect:** 9 outliers
- **Negative affect:** 31 outliers
## Clustering Analysis
Cluster Labels:
| Cluster | Count |
|---------|-------|
| 0.0 | 982 |
| 2.0 | 789 |
| 1.0 | 326 |

## Categorical Data Analysis
### Unique Value Count for All Categorical Columns
| Column | Unique Value Count |
|---------|--------------------|
| Country name | 165 |

## Hierarchical Clustering
![Dendrogram](dendrogram.png)
## Visualizations
![Pairplot](pairplot.png)
Skipping distribution plot for Life Ladder because it has 1814 distinct values.
Skipping distribution plot for Log GDP per capita because it has 1760 distinct values.
Skipping distribution plot for Social support because it has 484 distinct values.
Skipping distribution plot for Healthy life expectancy at birth because it has 1126 distinct values.
Skipping distribution plot for Freedom to make life choices because it has 550 distinct values.
Skipping distribution plot for Generosity because it has 650 distinct values.
Skipping distribution plot for Perceptions of corruption because it has 613 distinct values.
Skipping distribution plot for Positive affect because it has 442 distinct values.
Skipping distribution plot for Negative affect because it has 394 distinct values.