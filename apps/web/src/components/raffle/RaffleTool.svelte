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

  let step = 1;

  let raffle: RaffleStatus | null = null;
  let selectedBranch: RaffleBranch | null = null;

  let loading = true;
  let error = "";

  let codesText = "";
  let validatingCodes = false;
  let validation: TicketBatchValidation | null = null;
  let codesError = "";

  let numbers: RaffleNumber[] = [];
  let loadingNumbers = false;
  let numbersError = "";
  let selectedNumberIds: number[] = [];

  let confirmingNumbers = false;
  let confirmError = "";
  let confirmedEntries: RaffleEntry[] = [];

  $: acceptedTickets = getAcceptedTickets(validation);

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

<section class="raffle">
  <StepIndicator currentStep={step} />

  {#if loading}
    <p class="muted">Cargando sorteo...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if raffle}
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
  {/if}
</section>

<style>
  .raffle {
    width: min(100%, 960px);
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .muted {
    margin: 0;
    color: rgba(255, 255, 255, 0.68);
  }

  .error {
    margin: 0;
    color: #ff7373;
  }

  @media (min-width: 760px) {
    .raffle {
      padding: 4rem 1.5rem;
    }
  }
</style>
