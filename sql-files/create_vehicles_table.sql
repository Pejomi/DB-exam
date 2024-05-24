IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Vehicles]')
                 AND type in (N'U'))
CREATE TABLE [dbo].[Vehicles]
(
    [vehicle_id]                 INT IDENTITY (1,1) PRIMARY KEY,
    [driver_id]                  INT,
    [age]                        INT,
    [make]                       VARCHAR(255),
    [model]                      VARCHAR(255),
    [vehicle_type]               VARCHAR(255),
    [hit_object_in_carriageway]  VARCHAR(255),
    [hit_object_off_carriageway] VARCHAR(255),
    [vehicle_manoeuvre]          VARCHAR(255),
    [point_of_impact]            VARCHAR(255)
);