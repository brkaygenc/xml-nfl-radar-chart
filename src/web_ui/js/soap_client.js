class NFLStatsClient {
    constructor(endpoint) {
        this.endpoint = endpoint;
        this.loadXSLT();
    }

    async loadXSLT() {
        const [playerListXSLT, radarChartXSLT] = await Promise.all([
            fetch('/xslt/player_list.xslt').then(r => r.text()),
            fetch('/xslt/radar_chart.xslt').then(r => r.text())
        ]);
        
        this.playerListTransform = new XSLTProcessor();
        this.playerListTransform.importStylesheet(new DOMParser().parseFromString(playerListXSLT, 'text/xml'));
        
        this.radarChartTransform = new XSLTProcessor();
        this.radarChartTransform.importStylesheet(new DOMParser().parseFromString(radarChartXSLT, 'text/xml'));
    }

    createSoapEnvelope(method, params) {
        return `<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:nfl="http://nfl.stats/soap">
            <soapenv:Header/>
            <soapenv:Body>
                <nfl:${method}>
                    ${Object.entries(params).map(([key, value]) => 
                        `<nfl:${key}>${value}</nfl:${key}>`).join('')}
                </nfl:${method}>
            </soapenv:Body>
        </soapenv:Envelope>`;
    }

    async callSoapMethod(method, params = {}) {
        const response = await fetch(this.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/xml;charset=UTF-8',
                'SOAPAction': `http://nfl.stats/soap#${method}`
            },
            body: this.createSoapEnvelope(method, params)
        });

        const xmlText = await response.text();
        return new DOMParser().parseFromString(xmlText, 'text/xml');
    }

    async getPlayersByPosition(position) {
        const xml = await this.callSoapMethod('get_players_by_position', { position });
        const fragment = this.playerListTransform.transformToFragment(xml, document);
        return fragment;
    }

    async getPositionStats(position) {
        const xml = await this.callSoapMethod('get_position_stats', { position });
        const fragment = this.radarChartTransform.transformToFragment(xml, document);
        return fragment;
    }

    async getTeams() {
        return this.callSoapMethod('get_teams');
    }

    async getTeamPoints(team) {
        return this.callSoapMethod('get_team_points', { team });
    }
} 