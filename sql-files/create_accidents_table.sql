IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Accidents]')
                 AND type in (N'U'))
CREATE TABLE [dbo].[Accidents]
(
    [accident_id]             INT IDENTITY (1,1) PRIMARY KEY,
    [vehicles_id]             INT,
    [severity]                VARCHAR(255),
    [date]                    DATE,
    [latitude]                DECIMAL,
    [longitude]               DECIMAL,
    [light_conditions]        VARCHAR(255),
    [number_of_casualties]    INT,
    [number_of_vehicles]      INT,
    [speed_limit]             INT,
    [time]                    DATETIME,
    [weather_conditions]      VARCHAR(255),
    [road_type]               VARCHAR(255),
    [road_surface_conditions] VARCHAR(255),
    [urban_or_rural_area]     VARCHAR(255)
);