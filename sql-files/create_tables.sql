IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[AgeBands]')
                 AND type in (N'U'))
CREATE TABLE AgeBands
(
    [age_band_ID] int IDENTITY PRIMARY KEY,
    [band]        varchar(50) NOT NULL,
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[AreaTypes]')
                 AND type in (N'U'))
CREATE TABLE AreaTypes
(
    [area_type_ID] int IDENTITY PRIMARY KEY,
    [type]         varchar(50) NOT NULL
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Collisions]')
                 AND type in (N'U'))
CREATE TABLE Collisions
(
    [collision_ID]               int IDENTITY PRIMARY KEY,
    [hit_object_in_carriageway]  varchar(50) NOT NULL,
    [hit_object_off_carriageway] varchar(50) NOT NULL,
    [vehicle_manoeuvre]          varchar(50) NOT NULL,
    [point_of_impact]            varchar(50) NOT NULL,
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Severities]')
                 AND type in (N'U'))
CREATE TABLE Severities
(
    [severity_ID] int IDENTITY PRIMARY KEY,
    [type]        varchar(50) NOT NULL
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Locations]')
                 AND type in (N'U'))
CREATE TABLE Locations
(
    [location_ID] int IDENTITY PRIMARY KEY,
    [latitude]    decimal(10, 6) NOT NULL,
    [longitude]   decimal(10, 6) NOT NULL,
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Environments]')
                 AND type in (N'U'))
CREATE TABLE EnvironmentConditions
(
    [environment_conditions_ID] int IDENTITY PRIMARY KEY,
    [light]                     varchar(50) NOT NULL,
    [weather]                   varchar(50) NOT NULL,
    [road_type]                 varchar(50) NOT NULL,
    [road_surface]              varchar(50) NOT NULL,
    [area_type_ID]              int          NOT NULL,
    [speed_limit]               int          NOT NULL,

    FOREIGN KEY ([area_type_ID]) REFERENCES AreaTypes (area_type_ID),
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Drivers]')
                 AND type in (N'U'))
CREATE TABLE Drivers
(
    [driver_ID]    int IDENTITY PRIMARY KEY,
    [age_band_ID]  int          NOT NULL,
    [sex]          varchar(50) NOT NULL,
    [area_type_ID] int          NOT NULL,

    FOREIGN KEY ([age_band_ID]) REFERENCES AgeBands (age_band_ID),
    FOREIGN KEY ([area_type_ID]) REFERENCES AreaTypes (area_type_ID),
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Vehicles]')
                 AND type in (N'U'))
CREATE TABLE Vehicles
(
    [vehicle_ID]   int IDENTITY PRIMARY KEY,
    [make]         varchar(50) NOT NULL,
    [model]        varchar(50) NOT NULL,
    [vehicle_type] int          NOT NULL,
    [model_year]   int          NOT NULL,
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Accidents]')
                 AND type in (N'U'))
CREATE TABLE Accidents
(
    [accident_ID]               int IDENTITY PRIMARY KEY,
    [vehicle_ ID]               int  NOT NULL,
    [driver_ID]                 int  NOT NULL,
    [severity_ID]               int  NOT NULL,
    [location_ID]               int  NOT NULL,
    [environment_conditions_ID] int  NOT NULL,
    [collision_ID]              int  NOT NULL,

    [date]                      date NOT NULL,
    [number_of_casualties]      int  NOT NULL,
    [number_of_vehicles]        int  NOT NULL,
    [time]                      time(0) NOT NULL,


    FOREIGN KEY ([vehicle_ ID]) REFERENCES Vehicles (vehicle_ID),
    FOREIGN KEY ([driver_ID]) REFERENCES Drivers (driver_ID),
    FOREIGN KEY ([severity_ID]) REFERENCES Severities (severity_ID),
    FOREIGN KEY ([location_ID]) REFERENCES Locations (location_ID),
    FOREIGN KEY ([environment_conditions_ID]) REFERENCES EnvironmentConditions (environment_conditions_ID),
    FOREIGN KEY ([collision_ID]) REFERENCES Collisions (collision_ID),
);