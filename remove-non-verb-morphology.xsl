<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml"/>

  <xsl:template match="/">
    <xsl:apply-templates select="root"/>
  </xsl:template>

  <xsl:template match="/">
    <c>
      <xsl:apply-templates select="root"/>
    </c>
  </xsl:template>

  <xsl:template match="img">
  </xsl:template>

  <xsl:template match="text">
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>
