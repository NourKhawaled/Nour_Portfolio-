------SQL

--1. The production manager asks for the following report:
SELECT ProductName as 'Name', ModelName as 'Model', 
ProductColor+', '+ProductSize+', '+ProductStyle as 'Properties',
ProductPrice as 'Price', ProductPrice-ProductCost as 'NetProfit'
FROM products 

--2. We updated the report from the previous section to include only large products (L) or products in color Black, white, red. 
---In addition, add a column named ProfitMargin that will show the percentage of profit The net relative to the price:
SELECT ProductName as 'Name', ModelName as 'Model', 
ProductColor+', '+ProductSize+', '+ProductStyle as 'Properties',
ProductPrice as 'Price', ProductPrice-ProductCost as 'NetProfit',
round((ProductPrice-ProductCost)/ProductPrice,2) as 'ProfitMargin'
FROM products 
WHERE ProductSize = 'L'or ProductColor in ('Black', 'White', 'Red')

--3. The marketing manager wants to know how many units were sold in total in the second half of 2016
---And several different orders were made during this period:
SELECT sum(OrderQuantity) as 'Total_Units_Sold', count(distinct OrderNumber) as 'Total_Orders_Made'
FROM sales.Sales
where OrderDate between '2016-07-01' and '2016-12-31'

--4. The factory is interested in reducing production lines with less relevant products. Find a few
---No products sold at all during 2017:
SELECT count(ProductID) as 'Unsold_Products'
from Products 
WHERE ProductID not in (
                        SELECT distinct p.ProductID
                        from  sales.Sales s join Products p
                        on s.ProductID = p.ProductID
                        where year(OrderDate) = '2017'
)

--5. Display the number of rows from the sales table for each status (Status_Order) for
---Lines where the quantity purchased (OrderQuantity) is greater than -1 omitted the lines
---marked with OK status.:
select Order_Status, count(Order_Status) as 'Row_Count'
FROM sales.sales 
WHERE orderQuantity > 1 and not Order_Status = 'ok'
group by Order_Status

--6. The factory's quality control manager wants to know which 3 products have a number
---Highest returns:
SELECT top 3 p.ProductName, sum(ReturnQuantity) as 'Total_Units_Returned'
from sales.Returns r JOIN Products p
on r.ProductID = p.ProductID
group BY p.ProductName
order BY sum(ReturnQuantity) desc 

--7. The marketing department wants to better understand our clientele. One of the reports
---What they are interested in seeing is the segmentation of the number of customers by level of education and gender. Omit
---From the report, customers who did not specify their gender:
select EducationLevel, Gender, count(CustomerID) as 'Number_of_Customers'
from sales.Customers
WHERE Gender is not NULL 
GROUP by EducationLevel, Gender

--8.  The company's VP of sales wants to know who the top 5 salespeople are.
---Salespeople are ranked simply by the number of units they have sold, regardless of the type of product or
---Its value.:
select top 5 st.FirstName, sum(OrderQuantity) as 'Total_Units_Sold'
from sales.Sales s join sales.Staff st 
on s.SoldBy = st.StaffMemberID
GROUP by st.FirstName
ORDER by sum(OrderQuantity) desc 

--9. D&R planning a new product line and want to know what is the most popular color?
---Show the color that sold the most units (products without paint will not be taken
---In the account):
select Top 1 p.ProductColor, sum(OrderQuantity) as 'Total_Units_Sold'
from sales.Sales s join Products p
on s.ProductID = p.ProductID
where p.ProductColor is not null
group by p.ProductColor

--10. In honor of the holidays, the customer retention representative wants to send a gift package
---For extremely loyal customers. Help her find the 10 clients* who brought the company into the company
---The highest amounts.:
SELECT top 10 c.FirstName+' '+c.LastName as 'CustomerName', round(sum(s.OrderQuantity*p.ProductPrice),2) as 'Total_Spend'
from sales.Customers c, sales.sales s, Products p
where c.CustomerID = s.CustomerKey and s.ProductID = p.ProductID
GROUP by c.CustomerID, c.FirstName+' '+c.LastName
ORDER by 'Total_Spend' desc 

--11. In order to plan a budget for the next year, you were asked to calculate the total production costs of each
---Category (for products sold only, no excess in stock):
SELECT c.CategoryName, round(sum(p.ProductCost*s.OrderQuantity),0) as 'Total_Cost'
from  sales.Sales s, Products p, subCategories subC, Categories c  
where s.ProductID = p.ProductID and subC.CategoryID = c.CategoryID and p.SubcategoryID=subC.SubcategoryID
GROUP by c.CategoryName
ORDER BY sum(p.ProductCost) desc

--12. The marketing department has developed a new campaign for the company's clothing products and wants to know when
---Best time of year to launch it. They want to know what is the weakest month
---per year in terms of the number of incoming orders and total units sold (is it the same
---This month?):
SELECT month(OrderDate) as 'Order_Month', count(month(OrderDate)) as 'Orders_made', sum(OrderQuantity) as 'Units_Sold'
FROM sales.sales
where ProductID IN ( select p.productID
                     from SubCategories sub, Categories c, products p 
                     where sub.CategoryID=c.CategoryID and p.SubcategoryID=sub.SubcategoryID and  c.CategoryName='clothing'
                                )
GROUP by month(OrderDate)
order by sum(OrderQuantity)






