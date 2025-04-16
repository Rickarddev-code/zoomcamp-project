{{ config(materialized='table') }}

WITH translated_data AS (
    SELECT 
        -- Translate 'Section' with its English translation from the label table
        d.English_translation AS Section,
        -- Translate 'Classification' with its English translation from the label table
        b.English_translation AS Classification,
        -- Translate 'Region' with its English translation from the label table
        c.English_translation AS Region,
        -- Retain 'Company Size' as is, no translation needed
        a.`Company Size`,  
        -- Change 2021 to 2022 for Year column by converting it to INT64 and using CASE
        CASE 
            WHEN CAST(a.Year AS INT64) = 2021 THEN 2022
            ELSE CAST(a.Year AS INT64)
        END AS Year,  -- Ensure the Year is INT64 after the change
        -- Include 'value_andel' and rename it to 'Percentage'
        a.value_andel AS Percentage
    FROM 
        `zoomcamp-456820.zoomcamp_ai.ai_adoption` AS a
    LEFT JOIN 
        {{ ref('label') }} AS b  -- Use the 'ref' function to refer to the label model
    ON a.Classification = b.ID  -- Join on Classification column
    LEFT JOIN
        {{ ref('label') }} AS c  -- Use the 'ref' function for the Region table
    ON a.Region = c.ID  -- Join on Region column
    LEFT JOIN
        {{ ref('label') }} AS d  -- Use the 'ref' function for the Section table
    ON a.Section = d.ID  -- Join on Section column for translation
)

SELECT * 
FROM translated_data
