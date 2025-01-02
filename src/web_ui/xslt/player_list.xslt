<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:nfl="http://nfl.stats/schemas/player">
    
    <xsl:template match="/">
        <div class="player-grid">
            <xsl:apply-templates select="//nfl:player"/>
        </div>
    </xsl:template>
    
    <xsl:template match="nfl:player">
        <div class="player-card">
            <h3><xsl:value-of select="nfl:playername"/></h3>
            <p>
                <xsl:value-of select="nfl:position"/> - 
                <xsl:value-of select="nfl:team"/>
            </p>
            <button class="add-button" onclick="selectPlayer('{nfl:playerid}', '{nfl:playername}', '{nfl:team}', '{nfl:position}')">
                Add to Compare
            </button>
        </div>
    </xsl:template>
</xsl:stylesheet> 