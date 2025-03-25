document.addEventListener('DOMContentLoaded', function() {
    const reportContent = document.getElementById('report-content');
    const latestScanReport = JSON.parse(localStorage.getItem('latestScanReport'));

    if (latestScanReport) {
        reportContent.innerHTML = `
            <p><strong>Type:</strong> ${latestScanReport.type}</p>
            <p><strong>Date:</strong> ${latestScanReport.date}</p>
            ${latestScanReport.type === 'Password Security' ? `
                <p><strong>Username:</strong> ${latestScanReport.username}</p>
                <p><strong>Password Strength:</strong> ${latestScanReport.strength}</p>
                <p><strong>Violations:</strong></p>
                <ul>
                    ${latestScanReport.violations.map(v => `<li>${v}</li>`).join('')}
                </ul>
            ` : `
                <p><strong>Website:</strong> ${latestScanReport.website}</p>
                <p><strong>DNS Info:</strong> ${latestScanReport.dnsInfo}</p>
                <p><strong>HTTPS Check:</strong> ${latestScanReport.httpsCheck}</p>
                <p><strong>Open Admin Pages:</strong> ${latestScanReport.openAdminPages}</p>
                <p><strong>Sensitive Information:</strong> ${latestScanReport.sensitiveInfo}</p>
            `}
        `;
    } else {
        reportContent.textContent = 'No report available';
    }
});