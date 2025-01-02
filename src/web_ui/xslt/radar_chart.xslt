<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:nfl="http://nfl.stats/schemas/player">
    
    <xsl:template match="/">
        <xsl:element name="script">
            var chartData = {
                players: [
                    <xsl:apply-templates select="//nfl:player"/>
                ]
            };
            updateRadarChart(chartData);
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="nfl:player">
        {
            playerid: '<xsl:value-of select="nfl:playerid"/>',
            playername: '<xsl:value-of select="nfl:playername"/>',
            team: '<xsl:value-of select="nfl:team"/>',
            position: '<xsl:value-of select="nfl:position"/>',
            stats: {
                <xsl:apply-templates select="nfl:stats/*"/>
            }
        }<xsl:if test="position() != last()">,</xsl:if>
    </xsl:template>
    
    <xsl:template match="nfl:stats/*">
        <xsl:value-of select="name()"/>: <xsl:value-of select="."/><xsl:if test="position() != last()">,</xsl:if>
    </xsl:template>
</xsl:stylesheet> 