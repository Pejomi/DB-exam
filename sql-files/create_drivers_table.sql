IF NOT EXISTS (SELECT *
               FROM sys.objects
               WHERE object_id = OBJECT_ID(N'[dbo].[Drivers]')
                 AND type in (N'U'))
CREATE TABLE [dbo].[Drivers]
(
    [driver_id]      INT IDENTITY (1,1) PRIMARY KEY,
    [age_band]       VARCHAR(50),
    [sex]            VARCHAR(50),
    [home_area_type] VARCHAR(255)
);