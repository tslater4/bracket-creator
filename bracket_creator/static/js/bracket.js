function startTournament(bracketPk, csrfToken) {
    var btn = document.getElementById('start-tournament-btn');
    if (btn) {
        btn.style.display = "none";
    }
    
    fetch(`/bracket/${bracketPk}/set_start/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === "ok") {
            location.reload();
        } else {
            if (btn) {
                btn.style.display = "";
            }
            console.error('Failed to start tournament');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (btn) {
            btn.style.display = "";
        }
    });
}

function initializeBracket(teams) {
    console.log('Initializing bracket with teams:', teams);
    
    if (typeof $ !== 'undefined' && $.fn.bracket && teams && teams.length > 0) {
        try {
            $('#bracket-container').bracket({
                init: {
                    teams: teams,
                    results: []
                },
                save: function(data, userData) {
                    console.log('Bracket updated:', data);
                }
            });
            console.log('Bracket initialized successfully');
        } catch (error) {
            console.error('Error initializing bracket:', error);
            document.getElementById('bracket-container').innerHTML = '<p>Error loading bracket: ' + error.message + '</p>';
        }
    } else {
        console.error('Cannot initialize bracket');
        console.log('jQuery available:', typeof $ !== 'undefined');
        console.log('Bracket plugin available:', typeof $.fn !== 'undefined' && typeof $.fn.bracket !== 'undefined');
        console.log('Teams:', teams);
        
        var container = document.getElementById('bracket-container');
        if (container) {
            container.innerHTML = '<p>Unable to load bracket. Check console for errors.</p>';
        }
    }
}