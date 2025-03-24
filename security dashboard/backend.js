document.addEventListener("DOMContentLoaded", function() {
    const reportContent = document.getElementById("report-content");
    
    function fetchReport() {
        // Simulating fetching data (Replace with real API call or local storage retrieval)
        const dummyReport = "Web Scanner found 2 vulnerabilities. No critical issues detected.";
        reportContent.textContent = dummyReport;
    }
    
    fetchReport();
});
