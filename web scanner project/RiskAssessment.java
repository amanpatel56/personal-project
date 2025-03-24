
public class RiskAssessment {
    
    public static void printRiskLevel(RiskLevel risk) {
        switch (risk) {
            case LOW:
                System.out.println("Low risk: Minor issue, unlikely to cause significant harm.");
                break;
            case MEDIUM:
                System.out.println("Medium risk: Moderate issue, needs attention to prevent exploitation.");
                break;
            case HIGH:
                System.out.println("High risk: Critical vulnerability, immediate action required.");
                break;
        }
    }

    public static RiskLevel assessRisk(String response) {
        if (response.contains("HTTP/1.1 200 OK") && response.contains("admin")) {
            return RiskLevel.HIGH;  // Admin page exposed
        } else if (response.contains("HTTP/1.1 302 Found") || response.contains("HTTP/1.1 403 Forbidden")) {
            return RiskLevel.MEDIUM;  // Possibly exposed admin page or misconfiguration
        } else if (response.contains("api_key") || response.contains("password")) {
            return RiskLevel.HIGH;  // Sensitive info exposed
        }
        return RiskLevel.LOW;  // Default low risk
    }
}
