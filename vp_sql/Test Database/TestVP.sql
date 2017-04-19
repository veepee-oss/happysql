USE [master]
go
/****** Object:  Database [TestVP]    Script Date: 04/04/2017 13:46:47 ******/
CREATE DATABASE [TestVP]
go
ALTER DATABASE [TestVP] SET COMPATIBILITY_LEVEL = 130
go
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [TestVP].[dbo].[sp_fulltext_database] @action = 'enable'
end
go
ALTER DATABASE [TestVP] SET ANSI_NULL_DEFAULT OFF 
go
ALTER DATABASE [TestVP] SET ANSI_NULLS OFF 
go
ALTER DATABASE [TestVP] SET ANSI_PADDING OFF 
go
ALTER DATABASE [TestVP] SET ANSI_WARNINGS OFF 
go
ALTER DATABASE [TestVP] SET ARITHABORT OFF 
go
ALTER DATABASE [TestVP] SET AUTO_CLOSE OFF 
go
ALTER DATABASE [TestVP] SET AUTO_SHRINK OFF 
go
ALTER DATABASE [TestVP] SET AUTO_UPDATE_STATISTICS ON 
go
ALTER DATABASE [TestVP] SET CURSOR_CLOSE_ON_COMMIT OFF 
go
ALTER DATABASE [TestVP] SET CURSOR_DEFAULT  GLOBAL 
go
ALTER DATABASE [TestVP] SET CONCAT_NULL_YIELDS_NULL OFF 
go
ALTER DATABASE [TestVP] SET NUMERIC_ROUNDABORT OFF 
go
ALTER DATABASE [TestVP] SET QUOTED_IDENTIFIER OFF 
go
ALTER DATABASE [TestVP] SET RECURSIVE_TRIGGERS OFF 
go
ALTER DATABASE [TestVP] SET  DISABLE_BROKER 
go
ALTER DATABASE [TestVP] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
go
ALTER DATABASE [TestVP] SET DATE_CORRELATION_OPTIMIZATION OFF 
go
ALTER DATABASE [TestVP] SET TRUSTWORTHY OFF 
go
ALTER DATABASE [TestVP] SET ALLOW_SNAPSHOT_ISOLATION OFF 
go
ALTER DATABASE [TestVP] SET PARAMETERIZATION SIMPLE 
go
ALTER DATABASE [TestVP] SET READ_COMMITTED_SNAPSHOT OFF 
go
ALTER DATABASE [TestVP] SET HONOR_BROKER_PRIORITY OFF 
go
ALTER DATABASE [TestVP] SET RECOVERY FULL 
go
ALTER DATABASE [TestVP] SET  MULTI_USER 
go
ALTER DATABASE [TestVP] SET PAGE_VERIFY CHECKSUM  
go
ALTER DATABASE [TestVP] SET DB_CHAINING OFF 
go
ALTER DATABASE [TestVP] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
go
ALTER DATABASE [TestVP] SET TARGET_RECOVERY_TIME = 60 SECONDS 
go
ALTER DATABASE [TestVP] SET DELAYED_DURABILITY = DISABLED 
go
ALTER DATABASE [TestVP] SET QUERY_STORE = OFF
go
USE [TestVP]
go
ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 0;
go
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET MAXDOP = PRIMARY;
go
ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = OFF;
go
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET LEGACY_CARDINALITY_ESTIMATION = PRIMARY;
go
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = ON;
go
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET PARAMETER_SNIFFING = PRIMARY;
go
ALTER DATABASE SCOPED CONFIGURATION SET QUERY_OPTIMIZER_HOTFIXES = OFF;
go
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET QUERY_OPTIMIZER_HOTFIXES = PRIMARY;
go
USE [TestVP]
go
/****** Object:  Table [dbo].[Rois_de_France]    Script Date: 04/04/2017 13:46:47 ******/
SET ANSI_NULLS ON
go
SET QUOTED_IDENTIFIER ON
go
CREATE TABLE [dbo].[Rois_de_France](
	[Id] [int] NOT NULL,
	[Nom] [text] NOT NULL,
	[Nom_de_naissance] [text] NULL,
	[Dynastie] [text] NOT NULL,
	[Date_de_naissance] [date] NULL,
	[Date_de_couronnement] [date] NULL,
	[Lieu_de_couronnement] [text] NULL,
	[Date_de_deces] [date] NULL,
	[Personnage_fictif] [bit] NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

go
INSERT [dbo].[Rois_de_France] ([Id], [Nom], [Nom_de_naissance], [Dynastie], [Date_de_naissance], [Date_de_couronnement], [Lieu_de_couronnement], [Date_de_deces], [Personnage_fictif]) VALUES (1, N'Louis XIV', N'Louis de Bourbon', N'Maison de Bourbon', CAST(N'1638-09-05' AS Date), CAST(N'1654-06-07' AS Date), N'Reims', CAST(N'1715-09-01' AS Date), 0)
INSERT [dbo].[Rois_de_France] ([Id], [Nom], [Nom_de_naissance], [Dynastie], [Date_de_naissance], [Date_de_couronnement], [Lieu_de_couronnement], [Date_de_deces], [Personnage_fictif]) VALUES (2, N'Charlemagne', NULL, N'Carolingiens', CAST(N'0742-04-02' AS Date), CAST(N'0800-12-25' AS Date), N'Rome', CAST(N'0814-01-28' AS Date), 0)
INSERT [dbo].[Rois_de_France] ([Id], [Nom], [Nom_de_naissance], [Dynastie], [Date_de_naissance], [Date_de_couronnement], [Lieu_de_couronnement], [Date_de_deces], [Personnage_fictif]) VALUES (3, N'Bon Roi Dagobert', NULL, N'Mérovingiens', CAST(N'0602-01-01' AS Date), CAST(N'0629-10-18' AS Date), NULL, CAST(N'0638-01-19' AS Date), 1)
INSERT [dbo].[Rois_de_France] ([Id], [Nom], [Nom_de_naissance], [Dynastie], [Date_de_naissance], [Date_de_couronnement], [Lieu_de_couronnement], [Date_de_deces], [Personnage_fictif]) VALUES (4, N'Louis XVI', N'Louis-Auguste de France', N'Maison Bourbon', CAST(N'1754-08-23' AS Date), CAST(N'1775-06-11' AS Date), N'Reims', CAST(N'1793-01-21' AS Date), 0)
INSERT [dbo].[Rois_de_France] ([Id], [Nom], [Nom_de_naissance], [Dynastie], [Date_de_naissance], [Date_de_couronnement], [Lieu_de_couronnement], [Date_de_deces], [Personnage_fictif]) VALUES (5, N'Clovis 1er', NULL, N'Mérovingiens', CAST(N'0466-01-01' AS Date), CAST(N'4811-01-01' AS Date), N'Reims', CAST(N'0511-11-27' AS Date), 0)
USE [master]
go
ALTER DATABASE [TestVP] SET  READ_WRITE 
go
