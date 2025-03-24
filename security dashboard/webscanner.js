document.getElementById('web-scanner-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const website = document.getElementById('website').value;

    // Simulate a web scan
    const resultDiv = document.getElementById('scan-result');
    resultDiv.innerHTML = `<p>Scanning website: ${website}</p>`;

    // Simulate DNS Lookup
    setTimeout(() => {
        resultDiv.innerHTML += `
            <p><strong>DNS Lookup:</strong></p>
            <p>IP Address: 192.168.1.1</p>
            <p>Hostname: ${website}</p>
        `;
    }, 1000);

    // Simulate HTTPS Check
    setTimeout(() => {
        const isHttps = website.startsWith('https://');
        resultDiv.innerHTML += `
            <p><strong>HTTPS Check:</strong></p>
            <p>${isHttps ? 'GOOD: The website is using HTTPS.' : 'WARNING: The website is not using HTTPS. Data might not be encrypted.'}</p>
        `;
    }, 2000);

    // Simulate Open Admin Page Check
    setTimeout(() => {
        const adminPaths = ['/admin', '/dashboard', '/login', '/wp-admin'];
        const openAdminPages = adminPaths.filter(path => Math.random() > 0.5); // Randomly simulate open admin pages
        resultDiv.innerHTML += `
            <p><strong>Open Admin Page Check:</strong></p>
            <p>${openAdminPages.length > 0 ? 'Found open admin pages: ' + openAdminPages.join(', ') : 'No open admin pages found.'}</p>
        `;
    }, 3000);

    // Simulate Exposed Sensitive Information Check
    setTimeout(() => {
        const sensitiveInfoFound = Math.random() > 0.5; // Randomly simulate sensitive information exposure
        resultDiv.innerHTML += `
            <p><strong>Exposed Sensitive Information Check:</strong></p>
            <p>${sensitiveInfoFound ? 'WARNING: Exposed sensitive information found!' : 'No exposed sensitive information found.'}</p>
        `;
    }, 4000);

    // Final Scan Result
    setTimeout(() => {
        resultDiv.innerHTML += `<p>Scan complete.</p>`;

        // Store the latest scan report
        const report = {
            type: 'Web Scanner',
            website: website,
            dnsInfo: 'IP Address: 192.168.1.1, Hostname: ' + website,
            httpsCheck: isHttps ? 'GOOD: The website is using HTTPS.' : 'WARNING: The website is not using HTTPS. Data might not be encrypted.',
            openAdminPages: openAdminPages.length > 0 ? 'Found open admin pages: ' + openAdminPages.join(', ') : 'No open admin pages found.',
            sensitiveInfo: sensitiveInfoFound ? 'WARNING: Exposed sensitive information found!' : 'No exposed sensitive information found.',
            date: new Date().toLocaleString()
        };
        localStorage.setItem('latestScanReport', JSON.stringify(report));
    }, 5000);
});
