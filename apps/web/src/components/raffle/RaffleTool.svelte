<script lang="ts">
  import { onMount } from "svelte";
  import BranchStep from "./BranchStep.svelte";
  import CodesStep from "./CodesStep.svelte";
  import ConfirmStep from "./ConfirmStep.svelte";
  import NumbersStep from "./NumbersStep.svelte";
  import StepIndicator from "./StepIndicator.svelte";
  import SuccessStep from "./SuccessStep.svelte";
  import ValidationStep from "./ValidationStep.svelte";
  import {
    confirmNumbers,
    getBranchNumbers,
    getRaffleStatus,
    validateTicketCodes,
    type RaffleBranch,
    type RaffleEntry,
    type RaffleNumber,
    type RaffleStatus,
    type TicketBatchValidation,
    type TicketValidationResult,
  } from "../../lib/raffle";

  // Svelte 5 Runes para reactividad
  let step = $state(1);

  let raffle = $state<RaffleStatus | null>(null);
  let selectedBranch = $state<RaffleBranch | null>(null);

  let loading = $state(true);
  let error = $state("");

  let codesText = $state("");
  let validatingCodes = $state(false);
  let validation = $state<TicketBatchValidation | null>(null);
  let codesError = $state("");

  let numbers = $state<RaffleNumber[]>([]);
  let loadingNumbers = $state(false);
  let numbersError = $state("");
  let selectedNumberIds = $state<number[]>([]);

  let confirmingNumbers = $state(false);
  let confirmError = $state("");
  let confirmedEntries = $state<RaffleEntry[]>([]);

  // Derivadas reactivas de Svelte 5
  let acceptedTickets = $derived(getAcceptedTickets(validation));

  onMount(async () => {
    try {
      raffle = await getRaffleStatus();
    } catch (err) {
      error =
        err instanceof Error ? err.message : "No pudimos cargar el sorteo.";
    } finally {
      loading = false;
    }
  });

  function goToStep(nextStep: number) {
    step = nextStep;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function selectBranch(branch: RaffleBranch) {
    selectedBranch = branch;
    validation = null;
    codesText = "";
    selectedNumberIds = [];
    confirmedEntries = [];
    goToStep(2);
  }

  function parseCodes(text: string) {
    return text
      .split(/[\n,]+/)
      .map((code) => code.trim().toUpperCase())
      .filter(Boolean);
  }

  async function handleValidateCodes(nextCodesText: string) {
    if (!selectedBranch) return;

    codesText = nextCodesText;
    codesError = "";
    validation = null;

    const codes = parseCodes(codesText);

    if (codes.length === 0) {
      codesError = "Agrega al menos un código.";
      return;
    }

    if (codes.length > 10) {
      codesError = "Solo puedes validar hasta 10 boletos por carga.";
      return;
    }

    validatingCodes = true;

    try {
      validation = await validateTicketCodes(selectedBranch.id, codes);
      selectedNumberIds = [];
      goToStep(3);
    } catch (err) {
      codesError =
        err instanceof Error ? err.message : "No pudimos validar tus boletos.";
    } finally {
      validatingCodes = false;
    }
  }

  async function continueToNumbers() {
    if (!selectedBranch || !validation || validation.accepted_count === 0) {
      return;
    }

    loadingNumbers = true;
    numbersError = "";

    try {
      numbers = await getBranchNumbers(selectedBranch.id);
      selectedNumberIds = [];
      goToStep(4);
    } catch (err) {
      numbersError =
        err instanceof Error ? err.message : "No pudimos cargar los números.";
      goToStep(4);
    } finally {
      loadingNumbers = false;
    }
  }

  function continueToConfirm() {
    if (selectedNumberIds.length !== acceptedTickets.length) return;

    confirmError = "";
    goToStep(5);
  }

  async function handleConfirmNumbers() {
    if (!validation) return;

    confirmingNumbers = true;
    confirmError = "";

    const selections = acceptedTickets.map((ticket, index) => ({
      ticket_code_id: ticket.ticket_code_id as number,
      raffle_number_id: selectedNumberIds[index],
    }));

    try {
      confirmedEntries = await confirmNumbers(validation.batch_id, selections);
      goToStep(6);
    } catch (err) {
      confirmError =
        err instanceof Error
          ? err.message
          : "No pudimos confirmar tus números.";

      if (selectedBranch) {
        numbers = await getBranchNumbers(selectedBranch.id).catch(
          () => numbers,
        );
      }
    } finally {
      confirmingNumbers = false;
    }
  }

  function resetBranch() {
    selectedBranch = null;
    validation = null;
    codesText = "";
    codesError = "";
    numbers = [];
    selectedNumberIds = [];
    confirmedEntries = [];
    goToStep(1);
  }

  function restartFlow() {
    validation = null;
    codesText = "";
    codesError = "";
    numbers = [];
    selectedNumberIds = [];
    confirmedEntries = [];
    goToStep(2);
  }

  function getAcceptedTickets(
    currentValidation: TicketBatchValidation | null,
  ): TicketValidationResult[] {
    if (!currentValidation) return [];

    return currentValidation.results.filter(
      (result) => result.status === "accepted" && result.ticket_code_id,
    );
  }
</script>

<div class="w-full max-w-3xl mx-auto py-4 space-y-6">
  <!-- Cuenta pasos indicador -->
  <StepIndicator currentStep={step} />

  {#if loading}
    <div class="flex flex-col items-center justify-center py-20 gap-4">
      <div class="h-10 w-10 animate-spin rounded-full border-4 border-[#e67a25]/20 border-t-[#e67a25]"></div>
      <p class="text-xs font-black text-[#e67a25] tracking-widest uppercase animate-pulse">Cargando sorteo...</p>
    </div>
  {:else if error}
    <div class="p-5 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-sm font-bold shadow-sm" role="alert">
      <h3 class="font-black text-red-800 text-base mb-1">Error</h3>
      <p>{error}</p>
    </div>
  {:else if raffle}
    <!-- Contenedor animable para la transición de pasos -->
    <div class="animate-in fade-in slide-in-from-bottom-2 duration-300">
      {#if step === 1}
        <BranchStep {raffle} onSelect={selectBranch} />
      {:else if step === 2 && selectedBranch}
        <CodesStep
          {selectedBranch}
          bind:codesText
          loading={validatingCodes}
          error={codesError}
          onBack={resetBranch}
          onValidate={handleValidateCodes}
        />
      {:else if step === 3 && selectedBranch && validation}
        <ValidationStep
          {selectedBranch}
          {validation}
          onBack={() => goToStep(2)}
          onContinue={continueToNumbers}
        />
      {:else if step === 4}
        <NumbersStep
          {numbers}
          {acceptedTickets}
          bind:selectedNumberIds
          loading={loadingNumbers}
          error={numbersError}
          onBack={() => goToStep(3)}
          onContinue={continueToConfirm}
        />
      {:else if step === 5}
        <ConfirmStep
          {acceptedTickets}
          {numbers}
          {selectedNumberIds}
          loading={confirmingNumbers}
          error={confirmError}
          onBack={() => goToStep(4)}
          onConfirm={handleConfirmNumbers}
        />
      {:else if step === 6}
        <SuccessStep entries={confirmedEntries} onRestart={restartFlow} />
      {/if}
    </div>
  {/if}
</div>
