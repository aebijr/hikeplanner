<script>
    import { browser, dev } from "$app/environment";
    import { onMount } from "svelte";

    let url = dev ? "http://localhost:5000" : "";
    if (!dev && browser) {
        url = location.protocol + "//" + location.host;
    }

    let downhill = 300;
    let uphill = 700;
    let length = 10000;

    let prediction = "n.a.";
    let linearPrediction = "n.a.";
    let din33466 = "n.a.";
    let sac = "n.a.";

    let debounceId;

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
        prediction = data.time;
        linearPrediction = data.linear;
        din33466 = data.din33466;
        sac = data.sac;
    }

    onMount(() => {
        predict();
    });

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
    <title>HikePlanner <strong>TEST</strong></title>
</svelte:head>

<div class="app-bg">
    <main class="container py-5">
        <div class="row g-4 align-items-start align-items-lg-stretch">
            <div class="col-lg-6">
                <div
                    class="p-3 p-lg-4 shadow-sm rounded-4 h-100"
                    style="background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.25);"
                >
                    <h1 class="display-6 fw-bold mb-2">HikePlanner</h1>
                    <p class="text-muted mb-4">
                        Schätze die Gehzeit basierend auf Distanz und Höhenmetern.
                    </p>

                    <form class="vstack gap-3" on:submit|preventDefault={predict}>
                        <div>
                            <label class="form-label fw-semibold">Abwärts [m]</label>
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

                        <div>
                            <label class="form-label fw-semibold">Aufwärts [m]</label>
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

                        <div>
                            <label class="form-label fw-semibold">Distanz [m]</label>
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

                        <div class="d-grid">
                            <button type="submit" 
    style="
        width: 100%;
        padding: 8px 14px;
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
        cursor: pointer;
        transition: transform 0.2s ease;
    "
    onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(0, 123, 255, 0.4)';"
    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0, 123, 255, 0.3)';"
>
    Berechnen
</button>
                        </div>
                    </form>
                </div>
            </div>

            <div class="col-lg-6">
                <div
                    class="p-3 p-lg-4 shadow-sm rounded-4 h-100"
                    style="background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.25);"
                >
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h2 class="h5 mb-0 fw-semibold">Dauer</h2>
                    </div>

                    <div class="table-responsive">
                        <table
                            class="table table-sm align-middle mb-0"
                            style="--bs-table-bg: transparent; --bs-table-striped-bg: transparent; --bs-table-hover-bg: transparent;"
                        >
                            <tbody>
                                <tr>
                                    <td class="d-flex justify-content-between small px-0">
                                        <span>Model (Gradient Boosting Regressor)</span>
                                        <span class="fw-semibold">{prediction}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="d-flex justify-content-between small px-0">
                                        <span>Model (Linear Regression)</span>
                                        <span class="fw-semibold">{linearPrediction}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="d-flex justify-content-between small px-0">
                                        <span>DIN33466</span>
                                        <span class="fw-semibold">{din33466}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="d-flex justify-content-between small px-0">
                                        <span>SAC</span>
                                        <span class="fw-semibold">{sac}</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="d-flex align-items-center justify-content-between mb-3 mt-4">
                        <h2 class="h5 mb-0 fw-semibold">Tour-Überblick</h2>
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
                                    style="width: {Math.min(downhill / 10000 * 100, 100)}%; background: linear-gradient(90deg, #198754, #74c69d);"
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
                                    style="width: {Math.min(uphill / 10000 * 100, 100)}%; background: linear-gradient(90deg, #fd7e14, #ffb366);"
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
                                    style="width: {Math.min(length / 30000 * 100, 100)}%; background: linear-gradient(90deg, #0d6efd, #6ea8fe);"
                                ></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</div>