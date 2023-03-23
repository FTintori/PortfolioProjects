SELECT * FROM ['NashvilleHousing']

 -- Standardize Date Format (date has been formatted with time)
  
 ALTER TABLE ['NashvilleHousing']
 ADD SaleDateConv Date;

 UPDATE ['NashvilleHousing']
 SET SaleDateConv = CONVERT(Date,SaleDate)
 
 SELECT * FROM ['NashvilleHousing']
 
 -- Update Not Working properly
 --UPDATE ['NashvilleHousing']
 --SET SaleDate = CONVERT(Date,SaleDate);

   -- PROPERTY ADDRESS POPULATION (some rows have no address)

SELECT *
	FROM ['NashvilleHousing']
	WHERE PropertyAddress IS NULL
	ORDER BY ParcelID
		-- ParcelID column has 1:1 correlation with ProperyAddrss
		--Self-join table to assign propertyaddress to NULL value
		--when ParcelID matches with a row where propertyaddress is populated 
		--ISNULL will autopopulate the empty column (of table a)
SELECT a.ParcelID,b.ParcelID, a.PropertyAddress,b.PropertyAddress, ISNULL(a.PropertyAddress,b.PropertyAddress)
FROM ['NashvilleHousing'] a
JOIN ['NashvilleHousing'] b
ON a.ParcelID = b.ParcelID 
AND
a.[UniqueID ]<> b.[UniqueID ]
WHERE a.PropertyAddress is NULL
ORDER BY a.ParcelID
		-- update table with the method above.
UPDATE a
SET PropertyAddress = ISNULL(a.PropertyAddress,b.PropertyAddress)
FROM ['NashvilleHousing'] a
JOIN ['NashvilleHousing'] b
ON a.ParcelID = b.ParcelID 
AND
a.[UniqueID ]<> b.[UniqueID ]
WHERE a.PropertyAddress is NULL

		--reformatting address to have Address + City + State


			-- METHOD 1 uses CHARINDEX TO CUT THE STRING AT A COMMA

SELECT 
SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1) as Address,
SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress)) as City
FROM ['NashvilleHousing']

					--create 2 new columns with address and city individually

 ALTER TABLE ['NashvilleHousing']
 ADD Property_Address nvarchar(255)

 UPDATE ['NashvilleHousing']
 SET Property_Address = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1)

 ALTER TABLE ['NashvilleHousing']
 ADD Property_City nvarchar(255)

 UPDATE ['NashvilleHousing']
 SET Property_City = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress))


			-- METHOD 2 uses PARSNAME TO CUT THE STRING at a period. For this to work, commas need to be replaced by periods

SELECT
PARSENAME(REPLACE(OwnerAddress, ',','.') , 3)
,PARSENAME(REPLACE(OwnerAddress, ',','.') , 2)
,PARSENAME(REPLACE(OwnerAddress, ',','.') , 1)
FROM ['NashvilleHousing']

					--create 2 new columns with address and city individually

					
ALTER TABLE ['NashvilleHousing']
ADD Owner_Address nvarchar(255)

ALTER TABLE ['NashvilleHousing']
ADD Owner_City nvarchar(255)

ALTER TABLE ['NashvilleHousing']
ADD Owner_State nvarchar(255)

UPDATE ['NashvilleHousing']
SET Owner_Address = PARSENAME(REPLACE(OwnerAddress, ',','.') , 3)

UPDATE ['NashvilleHousing']
SET Owner_City = PARSENAME(REPLACE(OwnerAddress, ',','.') , 2)

UPDATE ['NashvilleHousing']
SET Owner_State = PARSENAME(REPLACE(OwnerAddress, ',','.') , 1)


		--SoldAsVacant uses both Y,N and Yes,No needs to be streamlined

			--The most popular choice is:	
SELECT DISTINCT(SoldAsVacant), Count(SoldAsVacant)
FROM ['NashvilleHousing']
GROUP BY SoldAsVacant
ORDER BY 2

		--Hence the least popular choice should be converted
SELECT SoldAsVacant
, CASE  When SoldAsVacant = 'Y' THEN 'Yes'
		When SoldAsVacant = 'N' THEN 'No'
		Else SoldAsVacant
		END
FROM ['NashvilleHousing']

UPDATE ['NashvilleHousing']
SET SoldAsVacant = CASE  When SoldAsVacant = 'Y' THEN 'Yes'
					When SoldAsVacant = 'N' THEN 'No'
					Else SoldAsVacant
					END



		-- Some lines are duplicated and need to be removed

WITH RowNumCTE AS(
SELECT *,
	ROW_NUMBER() OVER (
	PARTITION BY ParcelID,
				PropertyAddress,
				SaleDate,
				LegalReference
				ORDER BY 
					ParcelID
				) row_num
FROM ['NashvilleHousing']
)
DELETE
FROM RowNumCTE
WHERE row_num>1


			--Remove columns that were edited or are useless

ALTER TABLE ['NashvilleHousing']
DROP COLUMN OwnerAddress, TaxDistrict, PropertyAddress,	SaleDate