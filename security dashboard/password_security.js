document.getElementById('password-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Evaluate password strength
    const strength = evaluatePasswordStrength(password);
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <p>Password Strength: ${strength.strength}</p>
        <p>Violations:</p>
        <ul>
            ${strength.violations.map(v => `<li>${v}</li>`).join('')}
        </ul>
    `;

    // Add user to local storage if password is not weak
    if (strength.strength !== 'Weak') {
        const users = JSON.parse(localStorage.getItem('users')) || [];
        users.push({ username, password });
        localStorage.setItem('users', JSON.stringify(users));
    }

    // Store the latest scan report
    const report = {
        type: 'Password Security',
        username: username,
        strength: strength.strength,
        violations: strength.violations,
        date: new Date().toLocaleString()
    };
    localStorage.setItem('latestScanReport', JSON.stringify(report));
});

function evaluatePasswordStrength(password) {
    const strengthCriteria = {
        length: pwd => pwd.length >= 8,
        uppercase: pwd => /[A-Z]/.test(pwd),
        lowercase: pwd => /[a-z]/.test(pwd),
        digits: pwd => /\d/.test(pwd),
        special: pwd => /[@$!%*?&#]/.test(pwd),
    };

    const score = Object.values(strengthCriteria).reduce((acc, criteria) => acc + criteria(password), 0);
    const violations = [];
    if (!strengthCriteria.length(password)) violations.push("Password must be at least 8 characters long.");
    if (!strengthCriteria.uppercase(password)) violations.push("Password must contain at least one uppercase letter.");
    if (!strengthCriteria.lowercase(password)) violations.push("Password must contain at least one lowercase letter.");
    if (!strengthCriteria.digits(password)) violations.push("Password must contain at least one digit.");
    if (!strengthCriteria.special(password)) violations.push("Password must contain at least one special character.");

    let strength;
    if (score < 3) strength = 'Weak';
    else if (score === 3) strength = 'Moderate';
    else strength = 'Strong';

    return { strength, violations };
}
