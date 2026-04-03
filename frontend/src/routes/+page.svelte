<script>
    import { browser, dev } from "$app/environment";
    import { onMount } from "svelte";

    // API URL für lokal oder Deployment
    // - lokal: Flask läuft auf localhost:5000
    // - deployed: gleiche Domain wie Frontend
    let url = dev ? "http://localhost:5000" : "";

    if (!dev && browser) {
        url = location.protocol + "//" + location.host;
    }

    // Eingabewerte (Standardwerte beim Start)
    let downhill = 300;
    let uphill = 700;
    let length = 10000;

    // Vorhersagen / Vergleichswerte
    let prediction = "n.a.";
    let linearPrediction = "n.a.";
    let din33466 = "n.a.";
    let sac = "n.a.";

    // Daten für die Visualisierung des Modellvergleichs
    let chartData = [];

    // Für Debounce bei Slider-/Input-Änderungen
    // verhindert zu viele API Requests bei schneller Eingabe
    let debounceId;

    // Hilfsfunktion:
    // wandelt Zeitformat "hh:mm:ss" in Stunden (Float) um
    // wird für die Progressbar-Skalierung verwendet
    function timeToHours(t) {
        let parts = t.split(":");
        let h = Number(parts[0]);
        let m = Number(parts[1]);
        return h + m / 60;
    }

    // Default-Schwierigkeitsgrad
    let difficulty = { label: "n.a.", color: "#6c757d" };

    // Berechnet eine einfache Schwierigkeitsmetrik
    // basierend auf Höhenmetern und Distanz
    function getDifficulty(uphill, downhill, length) {
        const score = uphill + downhill + length / 10;

        if (score < 3000) return { label: "Leicht", color: "#198754" };
        if (score < 8000) return { label: "Mittel", color: "#ffc107" };
        return { label: "Schwer", color: "#dc3545" };
    }

    // Holt die Berechnung vom Backend
    // Backend liefert verschiedene Modelle zum Vergleich
    async function predict() {
        let result = await fetch(
            url +
                "/api/predict?" +
                new URLSearchParams({
                    downhill: downhill,
                    uphill: uphill,
                    length: length,
                }),
            {
                method: "GET",
            },
        );

        let data = await result.json();
        console.log(data);

        // Modellresultate
        prediction = data.time;
        linearPrediction = data.linear;
        din33466 = data.din33466;
        sac = data.sac;

        // Datenstruktur für Modellvergleich-Progressbars
        chartData = [
            {
                label: "Gradient Boosting",
                display: `${prediction} [h:m:s]`,
                value: timeToHours(prediction)
            },
            {
                label: "Linear Regression",
                display: `${linearPrediction} [h:m:s]`,
                value: timeToHours(linearPrediction)
            },
            {
                label: "DIN33466",
                display: `${din33466} [h:m:s]`,
                value: timeToHours(din33466)
            },
            {
                label: "SAC",
                display: `${sac} [h:m:s]`,
                value: timeToHours(sac)
            }
        ];

        // Schwierigkeitsgrad neu berechnen
        difficulty = getDifficulty(uphill, downhill, length);
    }

    // Initiale Berechnung beim Laden der Seite
    onMount(() => {
        predict();
    });

    // Verhindert zu viele Requests bei schneller Eingabe
    // (Debounce-Mechanismus)
    function schedulePredict() {
        if (debounceId) {
            clearTimeout(debounceId);
        }

        debounceId = setTimeout(() => {
            predict();
        }, 300);
    }
</script>

<svelte:head>
    <title>HikePlanner</title>
</svelte:head>

<div class="app-bg">
    <main class="container py-5">
        <div class="row g-4 align-items-start align-items-lg-stretch">

            <!-- Eingabeformular -->
            <div class="col-lg-6">
                <div
                    class="p-3 p-lg-4 shadow-sm rounded-4 h-100"
                    style="
                        background: rgba(255, 255, 255, 0.18);
                        backdrop-filter: blur(12px);
                        -webkit-backdrop-filter: blur(12px);
                        border: 1px solid rgba(255, 255, 255, 0.25);
                    "
                >
                    <h1 class="display-6 fw-bold mb-2">
                        HikePlanner
                    </h1>

                    <div class="d-flex justify-content-between small mb-3">
                                <span>Der HikePlanner berechnet deine Gehzeit durch die Kombination von Distanz und Höhenmetern. Neben den Standardberechnungen nach DIN 33466 oder dem SAC-Modell stehen dir Machine-Learning-Verfahren wie Gradient Boosting und Lineare Regression zur Verfügung, die auf echten Wanderdaten trainiert wurden.</span>
                    </div>

                    <form
                        class="vstack gap-3"
                        on:submit|preventDefault={predict}
                    >


                    <div class="d-flex align-items-center justify-content-between mb-0">
                        <h2 class="h5 mb-0 fw-semibold">Parameter</h2>
                    </div>

                        <!-- Abwärts Höhenmeter -->
                        <div>
                            <div class="d-flex justify-content-between small">
                                <span>Abwärts [m]</span>
                            </div>


                            <div class="row g-2 align-items-center">
                                <div class="col-4">
                                    <input
                                        type="number"
                                        class="form-control"
                                        bind:value={downhill}
                                        min="0"
                                        max="10000"
                                        on:input={schedulePredict}
                                    />
                                </div>

                                <div class="col-8">
                                    <input
                                        type="range"
                                        class="form-range"
                                        style="accent-color: #198754;"
                                        bind:value={downhill}
                                        min="0"
                                        max="10000"
                                        step="10"
                                        on:input={schedulePredict}
                                    />
                                </div>
                            </div>
                        </div>

                        <!-- Aufwärts Höhenmeter -->
                        <div>
                            <div class="d-flex justify-content-between small">
                                <span>Aufwärts [m]</span>
                            </div>

                            <div class="row g-2 align-items-center">
                                <div class="col-4">
                                    <input
                                        type="number"
                                        class="form-control"
                                        bind:value={uphill}
                                        min="0"
                                        max="10000"
                                        on:input={schedulePredict}
                                    />
                                </div>

                                <div class="col-8">
                                    <input
                                        type="range"
                                        class="form-range"
                                        style="accent-color: #fd7e14;"
                                        bind:value={uphill}
                                        min="0"
                                        max="10000"
                                        step="10"
                                        on:input={schedulePredict}
                                    />
                                </div>
                            </div>
                        </div>

                        <!-- Distanz -->
                        <div>
                            <div class="d-flex justify-content-between small">
                                <span>Distanz [m]</span>
                            </div>

                            <div class="row g-2 align-items-center">
                                <div class="col-4">
                                    <input
                                        type="number"
                                        class="form-control"
                                        bind:value={length}
                                        min="0"
                                        max="30000"
                                        on:input={schedulePredict}
                                    />
                                </div>

                                <div class="col-8">
                                    <input
                                        type="range"
                                        class="form-range"
                                        style="accent-color: #0d6efd;"
                                        bind:value={length}
                                        min="0"
                                        max="30000"
                                        step="10"
                                        on:input={schedulePredict}
                                    />
                                </div>
                            </div>
                        </div>

                        <!-- Submit-Button -->
                        <div class="d-grid">
                            <button
                                type="submit"
                                style="
                                    width: 100%;
                                    padding: 8px 14px;
                                    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                                    color: white;
                                    border: none;
                                    border-radius: 12px;
                                    font-size: 0.9rem;
                                    font-weight: 500;
                                    cursor: pointer;
                                    transition: transform 0.2s ease;
                                "
                            >
                                Berechnen
                            </button>
                        </div>

                    </form>
                </div>
            </div>

            <!-- Resultat / Visualisierung -->
            <div class="col-lg-6">
                <div
                    class="p-3 p-lg-4 shadow-sm rounded-4 h-100"
                    style="
                        background: rgba(255, 255, 255, 0.18);
                        backdrop-filter: blur(12px);
                        -webkit-backdrop-filter: blur(12px);
                        border: 1px solid rgba(255, 255, 255, 0.25);
                    "
                >

                    <!-- Resultatübersicht -->
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h2 class="h5 mb-0 fw-semibold">Modellvergleich</h2>
                    </div>

                    <!-- Modellvergleich -->
                    <div class="mt-2">
                        <div class="vstack gap-3">

                            {#each chartData as model}

                                <div>

                                    <div class="d-flex justify-content-between small">
                                        <span>{model.label}</span>
                                        <span>{model.display}</span>
                                    </div>

                                    <div class="progress" style="height: 8px;">
                                        <div
                                            class="progress-bar"
                                            style="
                                                width: {Math.min(model.value / 24 * 100, 100)}%;
                                                background: linear-gradient(90deg,#0d6efd,#6ea8fe);
                                            "
                                        ></div>
                                    </div>

                                </div>

                            {/each}

                        </div>
                    </div>

                    <!-- Visueller Überblick der Eingabewerte -->
                    <div class="d-flex align-items-center justify-content-between mb-3 mt-4">
                        <h2 class="h5 mb-0 fw-semibold">
                            Tour-Überblick
                        </h2>
                    </div>

                    <div class="vstack gap-3">

                        <!-- Abwärts -->
                        <div>
                            <div class="d-flex justify-content-between small">
                                <span>Abwärts</span>
                                <span>{(downhill / 1000).toFixed(1)} km</span>
                            </div>

                            <div class="progress" style="height: 6px;">
                                <div
                                    class="progress-bar"
                                    style="
                                        width: {Math.min(downhill / 10000 * 100, 100)}%;
                                        background: linear-gradient(90deg, #20c997, #63e6be)
                                    "
                                ></div>
                            </div>
                        </div>

                        <!-- Aufwärts -->
                        <div>
                            <div class="d-flex justify-content-between small">
                                <span>Aufwärts</span>
                                <span>{(uphill / 1000).toFixed(1)} km</span>
                            </div>

                            <div class="progress" style="height: 6px;">
                                <div
                                    class="progress-bar"
                                    style="
                                        width: {Math.min(uphill / 10000 * 100, 100)}%;
                                        background: linear-gradient(90deg, #fd7e14, #ffb366)
                                    "
                                ></div>
                            </div>
                        </div>

                        <!-- Distanz -->
                        <div>
                            <div class="d-flex justify-content-between small">
                                <span>Distanz</span>
                                <span>{(length / 1000).toFixed(1)} km</span>
                            </div>

                            <div class="progress" style="height: 6px;">
                                <div
                                    class="progress-bar"
                                    style="
                                        width: {Math.min(length / 30000 * 100, 100)}%;
                                        background: linear-gradient(90deg, #6f42c1, #b197fc)
                                    "
                                ></div>
                            </div>
                        </div>

                    </div>

                    <!-- Schwierigkeitsgrad -->
                    <div class="d-flex align-items-center justify-content-between mb-3 mt-4">
                        <h2 class="h5 mb-0 fw-semibold">
                            Schwierigkeitsgrad
                        </h2>
                    </div>

                    <div class="mt-2">

                        <div class="d-flex justify-content-between small">
                            <span>{difficulty.label}</span>
                        </div>

                        <div class="progress" style="height:6px;">
                            <div
                                class="progress-bar"
                                style="
                                    width: {difficulty.label === 'Leicht' ? '33%' :
                                            difficulty.label === 'Mittel' ? '66%' : '100%'};
                                    background: {difficulty.label === 'Leicht'
                                        ? 'linear-gradient(90deg, #198754, #74c69d)'
                                        : difficulty.label === 'Mittel'
                                        ? 'linear-gradient(90deg, #ffc107, #ffe066)'
                                        : 'linear-gradient(90deg, #dc3545, #f08080)'};
                                "
                            ></div>
                        </div>

                    </div>

                </div>
            </div>

        </div>
    </main>
</div>