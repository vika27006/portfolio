-- Суммарная выручка по категориям и регионам
SELECT 
    category,
    region,
    SUM(revenue) AS total_revenue,
    SUM(quantity_sold) AS total_quantity,
    COUNT(*) AS sales_count
FROM Sales
GROUP BY category, region
ORDER BY total_revenue DESC;

-- Продукты с выручкой > 10% от общей выручки
WITH total_revenue_all AS (
    SELECT SUM(revenue) AS total FROM Sales
)
SELECT 
    product, 
    SUM(revenue) AS total_revenue,
    ROUND(100.0 * SUM(revenue) / (SELECT total FROM total_revenue_all), 2) AS revenue_percent
FROM Sales
GROUP BY product
HAVING SUM(revenue) > (SELECT total * 0.1 FROM total_revenue_all)
ORDER BY total_revenue DESC;


-- GROUPING SETS: итоги по продуктам, категориям и общий итог
SELECT 
    product,
    category,
    SUM(revenue) AS total_revenue,
    GROUPING(product) AS is_product_total,
    GROUPING(category) AS is_category_total
FROM Sales
GROUP BY GROUPING SETS ((product), (category), ())
ORDER BY product NULLS LAST, category NULLS LAST;

-- Все возможные комбинации продукт-категория-регион
SELECT 
    COALESCE(product, 'Все продукты') AS product,
    COALESCE(category, 'Все категории') AS category,
    COALESCE(region, 'Все регионы') AS region,
    SUM(revenue) AS total_revenue
FROM Sales
GROUP BY CUBE (product, category, region)
ORDER BY product NULLS LAST, category NULLS LAST, region NULLS LAST;

-- Ранжирование продуктов по выручке
SELECT 
    product,
    SUM(revenue) AS total_revenue,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank,
    DENSE_RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_dense_rank,
    ROW_NUMBER() OVER (ORDER BY SUM(revenue) DESC) AS row_num
FROM Sales
GROUP BY product
ORDER BY total_revenue DESC;

-- Скользящая сумма выручки в разрезе категории и региона
SELECT 
    id,
    sale_date,
    category,
    region,
    product,
    revenue,
    SUM(revenue) OVER (PARTITION BY category, region ORDER BY sale_date) AS cumulative_revenue,
    AVG(revenue) OVER (PARTITION BY category, region ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS moving_avg_2
FROM Sales
ORDER BY category, region, sale_date;

-- Топ-2 продукта по продажам в каждом регионе
WITH ranked_products AS (
    SELECT 
        region,
        product,
        SUM(quantity_sold) AS total_quantity,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(quantity_sold) DESC) AS rn
    FROM Sales
    GROUP BY region, product
)
SELECT 
    region,
    product,
    total_quantity,
    rn AS rank_in_region
FROM ranked_products
WHERE rn <= 2
ORDER BY region, rn;
