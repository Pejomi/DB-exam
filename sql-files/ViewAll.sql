SELECT        dbo.Vehicles.make, dbo.Vehicles.model, dbo.Vehicles.type AS vehicle_type, dbo.Vehicles.model_year, dbo.AgeBands.band, dbo.Drivers.sex, AreaDrivers.home_area_type, dbo.Severities.type AS severity_type, 
                         dbo.EnvironmentConditions.light, dbo.EnvironmentConditions.weather, dbo.EnvironmentConditions.road_type, dbo.EnvironmentConditions.road_surface, AreaEnvironmentConditions.area_type, 
                         dbo.EnvironmentConditions.speed_limit, dbo.Collisions.hit_object_in_carriageway, dbo.Collisions.hit_object_off_carriageway, dbo.Collisions.vehicle_manoeuvre, dbo.Collisions.point_of_impact, dbo.Accidents.date, 
                         dbo.Accidents.number_of_casualties, dbo.Accidents.number_of_vehicles, dbo.Accidents.time, dbo.Accidents.latitude, dbo.Accidents.longitude
FROM            dbo.Accidents INNER JOIN
                         dbo.Collisions ON dbo.Accidents.collision_ID = dbo.Collisions.collision_ID INNER JOIN
                         dbo.Drivers ON dbo.Accidents.driver_ID = dbo.Drivers.driver_ID INNER JOIN
                         dbo.AreaTypes ON dbo.Drivers.area_type_ID = dbo.AreaTypes.area_type_ID INNER JOIN
                         dbo.AgeBands ON dbo.Drivers.age_band_ID = dbo.AgeBands.age_band_ID INNER JOIN
                         dbo.EnvironmentConditions ON dbo.Accidents.environment_conditions_ID = dbo.EnvironmentConditions.environment_conditions_ID AND dbo.AreaTypes.area_type_ID = dbo.EnvironmentConditions.area_type_ID INNER JOIN
                         dbo.Severities ON dbo.Accidents.severity_ID = dbo.Severities.severity_ID INNER JOIN
                         dbo.Vehicles ON dbo.Accidents.vehicle_ID = dbo.Vehicles.vehicle_ID INNER JOIN
                             (SELECT        type AS home_area_type, area_type_ID
                               FROM            dbo.AreaTypes AS AreaTypes_1) AS AreaDrivers ON dbo.Drivers.area_type_ID = AreaDrivers.area_type_ID INNER JOIN
                             (SELECT        type AS area_type, area_type_ID
                               FROM            dbo.AreaTypes AS AreaTypes_1) AS AreaEnvironmentConditions ON dbo.EnvironmentConditions.area_type_ID = AreaEnvironmentConditions.area_type_ID