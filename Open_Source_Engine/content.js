/**
 * @fileoverview AAP Client-Side Execution Bridge.
 * Intercepts DOM interactions, parses embedded AAP JSON-LD manifests,
 * and communicates with the Enterprise Data Plane for real-time telemetry and UI patching.
 */

// Use localhost to prevent loopback routing blocks in local environments
const ENTERPRISE_ENDPOINT = "http://localhost:8000/api/v1/trace";

console.log("[AAP Engine] Content script successfully injected into the page.");

/**
 * Scans the current document for an embedded AAP JSON-LD manifest.
 * @returns {Object|null} The parsed JSON manifest if found, otherwise null.
 */
function parseEmbeddedAAPManifest() {
  const scripts = document.querySelectorAll('script[type="application/ld+json"]');
  for (let script of scripts) {
    try {
      const data = JSON.parse(script.textContent);
      if (data["@type"] === "AgenticMap") {
        console.log("[AAP Engine] Valid open-standard manifest detected.");
        return data;
      }
    } catch (error) {
      continue;
    }
  }
  return null;
}

/**
 * Captures user interaction, cross-references it with local semantic manifests,
 * and requests runtime patches from the Enterprise platform.
 * @param {string} eventType - The type of DOM event (e.g., "click").
 * @param {HTMLElement} element - The DOM element targeted by the interaction.
 */
async function evaluateAndTrace(eventType, element) {
  console.log(`[AAP Engine] Interaction detected: ${eventType} on <${element.tagName.toLowerCase()}>`);
  
  const manifest = parseEmbeddedAAPManifest();
  const selector = `${element.tagName.toLowerCase()}${element.id ? '#' + element.id : ''}`;
  
  const payload = {
    url: window.location.href,
    eventType: eventType,
    targetSelector: selector,
    currentRole: element.getAttribute("role") || element.tagName.toLowerCase(),
    declaredIntent: null
  };

  if (manifest && manifest.elements) {
    const matched = manifest.elements.find(el => el.targetSelector === selector);
    if (matched) {
      payload.declaredIntent = matched.intent;
      console.log(`[AAP Engine] Matched intent in manifest: ${matched.intent}`);
    }
  }

  try {
    console.log("[AAP Engine] Sending telemetry payload to Enterprise Plane...");
    const response = await fetch(ENTERPRISE_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const result = await response.json();
    console.log("[AAP Engine] Telemetry processed. Response received:", result);
    
    if (result.active_patches && result.active_patches.length > 0) {
      result.active_patches.forEach(patch => {
        const el = document.querySelector(patch.selector);
        if (el) {
          // 1. Apply the invisible accessibility patches
          el.setAttribute("role", patch.corrected_role);
          el.setAttribute("aria-label", patch.corrected_label);
          console.log(`[AAP Engine] SUCCESS: Dynamically patched elements for selector: ${patch.selector}`);

          // 2. Add visual UI feedback for the demonstration
          if (!el.nextElementSibling || el.nextElementSibling.className !== "aap-feedback") {
            const feedback = document.createElement("span");
            feedback.className = "aap-feedback";
            feedback.textContent = " ✅ Processed & Accessibility Patched!";
            feedback.style.color = "#16a34a"; // Matches the green button
            feedback.style.fontWeight = "bold";
            feedback.style.marginLeft = "15px";
            feedback.style.fontFamily = "sans-serif";
            
            // Insert the message right after the button
            el.parentNode.insertBefore(feedback, el.nextSibling);
            
            // Automatically remove the message after 3 seconds
            setTimeout(() => {
              if (feedback.parentNode) feedback.remove();
            }, 2000);
          }
        }
      });
    }
  } catch (error) {
    console.error("[AAP Engine] Enterprise sync offline or failed.", error);
  }
}

// Global Event Listeners using capture phase to ensure interception
document.addEventListener("click", (e) => evaluateAndTrace("click", e.target), true);