IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[AgeBands]')
                 AND type in (N'U'))
CREATE TABLE AgeBands
(
    [age_band_ID] int IDENTITY PRIMARY KEY,
    [band]        varchar(50) NOT NULL,
    UNIQUE ([band])
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[AreaTypes]')
                 AND type in (N'U'))
CREATE TABLE AreaTypes
(
    [area_type_ID] int IDENTITY PRIMARY KEY,
    [type]         varchar(50) NOT NULL,
    UNIQUE ([type])
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Collisions]')
                 AND type in (N'U'))
CREATE TABLE Collisions
(
    [collision_ID]               int IDENTITY PRIMARY KEY,
    [hit_object_in_carriageway]  varchar(50),
    [hit_object_off_carriageway] varchar(50),
    [vehicle_manoeuvre]          varchar(50),
    [point_of_impact]            varchar(50),
    UNIQUE ([hit_object_in_carriageway], [hit_object_off_carriageway], [vehicle_manoeuvre], [point_of_impact])
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Severities]')
                 AND type in (N'U'))
CREATE TABLE Severities
(
    [severity_ID] int IDENTITY PRIMARY KEY,
    [type]        varchar(50) NOT NULL,
    UNIQUE ([type])
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Environments]')
                 AND type in (N'U'))
CREATE TABLE EnvironmentConditions
(
    [environment_conditions_ID] int IDENTITY PRIMARY KEY,
    [light]                     varchar(50),
    [weather]                   varchar(50),
    [road_type]                 varchar(50),
    [road_surface]              varchar(50),
    [area_type_ID]              int,
    [speed_limit]               int,

    FOREIGN KEY ([area_type_ID]) REFERENCES AreaTypes (area_type_ID),
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Drivers]')
                 AND type in (N'U'))
CREATE TABLE Drivers
(
    [driver_ID]    int IDENTITY PRIMARY KEY,
    [age_band_ID]  int NOT NULL,
    [sex]          varchar(50),
    [area_type_ID] int NOT NULL,

    FOREIGN KEY ([age_band_ID]) REFERENCES AgeBands (age_band_ID),
    FOREIGN KEY ([area_type_ID]) REFERENCES AreaTypes (area_type_ID),
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Vehicles]')
                 AND type in (N'U'))
CREATE TABLE Vehicles
(
    [vehicle_ID] int IDENTITY PRIMARY KEY,
    [make]       varchar(50),
    [model]      varchar(50),
    [type]       varchar(50),
    [model_year] int,
    UNIQUE ([make], [model], [type], [model_year])
);

IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Accidents]')
                 AND type in (N'U'))
CREATE TABLE Accidents
(
    [accident_ID]               int IDENTITY PRIMARY KEY,
    [vehicle_ID]                int NOT NULL,
    [driver_ID]                 int NOT NULL,
    [severity_ID]               int NOT NULL,
    [environment_conditions_ID] int NOT NULL,
    [collision_ID]              int NOT NULL,

    [date]                      date,
    [number_of_casualties]      int,
    [number_of_vehicles]        int,
    [time]                      time(0),
    [latitude]                  decimal(10, 6),
    [longitude]                 decimal(10, 6),

    FOREIGN KEY ([vehicle_ID]) REFERENCES Vehicles (vehicle_ID),
    FOREIGN KEY ([driver_ID]) REFERENCES Drivers (driver_ID),
    FOREIGN KEY ([severity_ID]) REFERENCES Severities (severity_ID),
    FOREIGN KEY ([environment_conditions_ID]) REFERENCES EnvironmentConditions (environment_conditions_ID),
    FOREIGN KEY ([collision_ID]) REFERENCES Collisions (collision_ID),
);