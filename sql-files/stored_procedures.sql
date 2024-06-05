CREATE PROCEDURE getSeverities
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_severities] 
		BEGIN TRY 
			SELECT DISTINCT type 
			FROM exam_schema_v3.dbo.Severities 
			ORDER BY type ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_severities] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getMaxCasualties
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_max_casualties] 
		BEGIN TRY 
			SELECT MAX(number_of_casualties) AS max_casualties 
			FROM dbo.Accidents 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_max_casualties]
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getMaxAndMinDates
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_max_and_min_dates] 
		BEGIN TRY
			SELECT MIN(date) AS min_date, MAX(date) AS max_date
			FROM dbo.Accidents
		END TRY
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_max_and_min_dates] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getHitObjectInCarriageway
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_hit_object_in_carriage_way]
		BEGIN TRY 
			SELECT DISTINCT hit_object_in_carriageway
			FROM dbo.Collisions 
			ORDER BY hit_object_in_carriageway ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_hit_object_in_carriage_way]
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getHitObjectOffCarriageway
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_hit_object_off_carriage_way]
		BEGIN TRY
			SELECT DISTINCT hit_object_off_carriageway
			FROM dbo.Collisions
			ORDER BY hit_object_off_carriageway ASC
		END TRY
		BEGIN CATCH
			ROLLBACK TRANSACTION [get_hit_object_off_carriage_way]
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getVehicleManoeuvre
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_vehicle_manoeuvre]
		BEGIN TRY 
			SELECT DISTINCT vehicle_manoeuvre
			FROM dbo.Collisions
			ORDER BY vehicle_manoeuvre ASC 
		END TRY 
		BEGIN CATCH
			ROLLBACK TRANSACTION [get_vehicle_manoeuvre] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getPointOfImpacts
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_point_of_impacts]
		BEGIN TRY 
			SELECT DISTINCT point_of_impact 
			FROM dbo.Collisions 
			ORDER BY point_of_impact ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_point_of_impacts]
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getSex
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_sex]
		BEGIN TRY 
			SELECT DISTINCT sex 
			FROM dbo.Drivers 
			ORDER by sex ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_sex] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getAgeBands
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_age_bands] 
		BEGIN TRY 
			SELECT DISTINCT band 
			FROM dbo.AgeBands 
			ORDER BY band ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_age_bands] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getAreaTypes
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_area_types] 
		BEGIN TRY 
			SELECT DISTINCT type 
			FROM dbo.AreaTypes 
			ORDER BY type ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_area_types] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getVehicleMake
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_vehicle_make] 
		BEGIN TRY 
			SELECT DISTINCT make 
			FROM dbo.Vehicles 
			ORDER BY make ASC
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_vehicle_make] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getVehicleModel
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_vehicle_model] 
		BEGIN TRY
			SELECT DISTINCT model 
			FROM dbo.Vehicles
			ORDER BY model ASC 
		END TRY
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_vehicle_model]
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getVehicleType
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_vehicle_type] 
		BEGIN TRY 
			SELECT DISTINCT type 
			FROM dbo.Vehicles 
			ORDER BY type ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_vehicle_type] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getVehicleModelYear
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_vehicle_model_year] 
		BEGIN TRY 
			SELECT DISTINCT model_year 
			FROM dbo.Vehicles 
			ORDER BY model_year ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_vehicle_model_year] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getWeather
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_weather] 
		BEGIN TRY 
			SELECT DISTINCT weather 
			FROM dbo.EnvironmentConditions 
			ORDER BY weather ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_weather] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getRoadTypes
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_road_types] 
		BEGIN TRY 
			SELECT DISTINCT road_type 
			FROM dbo.EnvironmentConditions 
			ORDER BY road_type ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_road_types] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getSpeedLimits
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_speed_limits]
		BEGIN TRY
			SELECT DISTINCT speed_limit
			FROM dbo.EnvironmentConditions 
			ORDER BY speed_limit ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_speed_limits] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getLights
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_lights] 
		BEGIN TRY 
			SELECT DISTINCT light 
			FROM dbo.EnvironmentConditions 
			ORDER BY light ASC 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_lights] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getRoadSurfaces
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_road_surfaces]
		BEGIN TRY
			SELECT DISTINCT road_surface 
			FROM dbo.EnvironmentConditions 
			ORDER BY road_surface ASC 
		END TRY
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_road_surfaces] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE countRows
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [count_rows] 
		BEGIN TRY 
			SELECT COUNT(*) AS count 
			FROM dbo.ViewAll
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [count_rows] 
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getAllColumns
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_all_columns]
		BEGIN TRY
			SELECT TOP(1) *
			FROM dbo.ViewAll
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_all_columns]
		END CATCH
	COMMIT
GO

CREATE PROCEDURE getAllData
AS   
	SET NOCOUNT ON
	BEGIN TRANSACTION [get_all_data] 
		BEGIN TRY 
			SELECT * 
			FROM dbo.ViewAll 
		END TRY 
		BEGIN CATCH 
			ROLLBACK TRANSACTION [get_all_data] 
		END CATCH
	COMMIT
GO