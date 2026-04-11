# === Base runtime ===
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 8080

# === Build stage ===
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src

# 1. Copy Solution and Project files
COPY . .
COPY ["API.Presentation/API.Presentation.csproj", "API.Presentation/"]

# 2. Restore dependencies for the solution
RUN dotnet restore "API.Presentation/API.Presentation.csproj"

# 4. Publish the specific API project
WORKDIR "/src/API.Presentation"
RUN dotnet publish "API.Presentation.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

# === Final runtime stage ===
FROM base AS final
WORKDIR /app

# 5. Copy the published output
COPY --from=build /app/publish .

ENTRYPOINT ["dotnet", "API.Presentation.dll"]