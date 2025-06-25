// script.js - Frontend for Aether's Conceptual Compass

document.addEventListener('DOMContentLoaded', () => {
    console.log('Aether frontend initialized');
    
    const userQueryInput = document.getElementById('userQuery');
    const analyzeButton = document.getElementById('analyzeBtn');
    const resultsDiv = document.getElementById('results');

    // Backend endpoint - using 127.0.0.1 to match the origin
    const BACKEND_ENDPOINT = 'http://127.0.0.1:5000/analyze';
    console.log('Using backend endpoint:', BACKEND_ENDPOINT);

    // Set initial message
    resultsDiv.innerHTML = '<p>Enter your query and click the button to analyze</p>';

    analyzeButton.addEventListener('click', async () => {
        const queryText = userQueryInput.value.trim();
        
        if (!queryText) {
            resultsDiv.innerHTML = '<p style="color: red;">Please enter a query to analyze.</p>';
            return;
        }

        // Show loading state
        resultsDiv.innerHTML = '<p>Analyzing your query... <span class="loading">⏳</span></p>';

        try {
            console.log('Sending request to:', BACKEND_ENDPOINT);
            console.log('Query:', queryText);
            
            const response = await fetch(BACKEND_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ query: queryText })
            });

            console.log('Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server responded with status ${response.status}: ${errorText}`);
            }

            const data = await response.json();
            console.log('Response data:', data);
            
            if (data.status === 'success' && data.conceptual_insight_report) {
                // Get the raw insight content
                let insightContent = String(data.conceptual_insight_report);
                
                // Simple formatting - preserve line breaks and basic formatting
                insightContent = insightContent
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\n/g, '<br>');
                
                // Display the formatted insight
                resultsDiv.innerHTML = `
                    <div class="result-section">
                        <div class="insight-content">
                            ${insightContent}
                        </div>
                    </div>
                `;
            } else {
                throw new Error(data.message || 'No insight was generated');
            }
        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = `
                <div style="color: red;">
                    <p>Failed to get analysis. Please try again.</p>
                    <p><small>${error.message}</small></p>
                </div>`;
        }
    });

    // Optional: Allow pressing Enter to trigger analysis in the textarea
    userQueryInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) { // Shift+Enter for new line
            event.preventDefault(); // Prevent default Enter behavior (e.g., new line)
            analyzeButton.click(); // Programmatically click the button
        }
    });
});