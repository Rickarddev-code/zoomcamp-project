{{ config(materialized='table') }}

WITH combined_data AS (
    SELECT 
        string_field_0 AS ID,
        -- Slå ihop kolumn 2 till 8 till en enda kolumn för svenska översättningar
        CONCAT(
            COALESCE(string_field_1, ''), ' ',
            COALESCE(string_field_2, ''), ' ',
            COALESCE(string_field_3, ''), ' ',
            COALESCE(string_field_4, ''), ' ',
            COALESCE(string_field_5, ''), ' ',
            COALESCE(CAST(double_field_6 AS STRING), ''), ' ',
            COALESCE(string_field_7, '')
        ) AS Swedish_translation
    FROM 
        `zoomcamp-456820.zoomcamp_ai.labels_table`
),

translated_labels AS (
    SELECT 
        ID,
        Swedish_translation,
        -- Normalize the ID by removing spaces and special characters before translation
        CASE 
            WHEN REPLACE(REPLACE(TRIM(ID), ' ', ''), '+', '') = '69-82+95.1exkl.75' THEN 'Other Service Companies (SNI 69-74, 77-82, 95.1)'
            WHEN REPLACE(REPLACE(TRIM(ID), ' ', ''), '+', '') = '69-75 77-82 95.1' THEN 'Other Service Companies (SNI 69-75, 77-82, 95.1)'
            WHEN ID = 'A01' THEN 'Marketing or Sales'
            WHEN ID = 'A02' THEN 'Production or Service Processes'
            WHEN ID = 'A03' THEN 'Organization of Business Administrative Processes or Corporate Management'
            WHEN ID = 'A04' THEN 'Logistics'
            WHEN ID = 'A05' THEN 'IT Security'
            WHEN ID = 'A06' THEN 'Accounting, Controlling or Financial Management'
            WHEN ID = 'A07' THEN 'Research and Development (R&D) or Innovation Activities'
            WHEN ID = 'Tot250' THEN 'Total 10 or More Employees'
            WHEN ID = '10-49' THEN '10-49 Employees'
            WHEN ID = '50-249' THEN '50-249 Employees'
            WHEN ID = '250-' THEN '250 or More Employees'
            WHEN ID = 'TotSNI' THEN 'All Companies'
            WHEN ID = '10-33' THEN 'Manufacturing Industry'
            WHEN ID = '35-39' THEN 'Energy and Recycling'
            WHEN ID = '41-43' THEN 'Construction Industry'
            WHEN ID = '45-47' THEN 'Trade, Service Workshops'
            WHEN ID = '49-53' THEN 'Transport and Storage'
            WHEN ID = '55-56' THEN 'Hotels and Restaurants'
            WHEN ID = '58-63' THEN 'Information and Communication'
            WHEN ID = '68' THEN 'Real Estate'
            WHEN ID = 'IKT' THEN 'ICT (Information and Communication Technology)'
            WHEN ID = 'SE' THEN 'Sweden'
            WHEN ID = 'RIKS1' THEN 'Stockholm County'
            WHEN ID = 'RIKS2' THEN 'Eastern Middle Sweden' 
            WHEN ID = 'RIKS3' THEN 'Smaland' 
            WHEN ID = 'RIKS4' THEN 'Southern Sweden'
            WHEN ID = 'RIKS5' THEN 'Western Sweden'
            WHEN ID = 'RIKS6' THEN 'Northern Middle Sweden'
            WHEN ID = 'RIKS7' THEN 'Central Norrland'
            WHEN ID = 'RIKS8' THEN 'Upper Norrland'
            WHEN ID = '0000034S' THEN 'Share, Percentage'
            WHEN ID = '0000034T' THEN 'Margin of Error, ±'
            WHEN ID = '2021' THEN '2021'
            WHEN ID = '2023' THEN '2023'
            WHEN ID = '2024' THEN '2024'
            ELSE 'No translation available'
        END AS English_translation
    FROM combined_data
)

SELECT ID, 
       Swedish_translation, 
       English_translation
FROM translated_labels
