import { AdjustmentsHorizontalIcon } from "@heroicons/react/24/solid";
import { Dialog, Transition, Switch } from "@headlessui/react";
import { Dispatch, Fragment, SetStateAction, useEffect, useState } from "react";
import axios from "axios";

interface Props {
  refreshValue: boolean;
  refresher: Dispatch<SetStateAction<boolean>>;
}

function Config({ refreshValue, refresher }: Props) {
  const [isOpen, setIsOpen] = useState(false);
  const [allSelection, setAllSelection] = useState(true);
  const [pearsonSelection, setPearsonSelection] = useState(false);
  const [countRanking, setCountRanking] = useState(true);
  const [pearsonRanking, setPearsonRanking] = useState(false);
  const [selection, setSelection] = useState("");
  const [ranking, setRanking] = useState("");
  const [limit, setLimit] = useState("10");

  function closeModal() {
    setIsOpen(false);
  }
  function openModal() {
    setIsOpen(true);
  }

  function handleSave(): void {
    const newConfig = { selection: selection, ranking: ranking, limit: limit };

    axios
      .post("http://127.0.0.1:8000/api/set-config/", newConfig)
      .then((response) => {
        console.log("Respuesta del servidor:", response.data);
        refresher(!refreshValue);
        closeModal();
      })
      .catch((error) => {
        console.error("Error (POST):", error);
      });

    closeModal();
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/get-config/"
        );
        console.log(
          `El server me dijo: selection(${response.data["selection"]}), ranking(${response.data["ranking"]})`
        );
        setSelection(response.data["selection"]);
        setRanking(response.data["ranking"]);
        setLimit(response.data["limit"]);

        if (response.data["selection"] == "pearson") {
          setAllSelection(false);
          setPearsonSelection(true);
        }
        if (response.data["ranking"] == "pearson_based_prediction") {
          setCountRanking(false);
          setPearsonRanking(true);
        }
      } catch (error) {
        console.error("Error (GET):", error);
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (allSelection) {
      setSelection("all");
    } else {
      setSelection("pearson");
    }
  }, [allSelection]);

  useEffect(() => {
    if (countRanking) {
      setRanking("count");
    } else {
      setRanking("pearson_based_prediction");
    }
  }, [countRanking]);

  function switchSelection(): void {
    if (pearsonRanking) {
      setPearsonRanking(false);
      setCountRanking(true);
    }
    setAllSelection(!allSelection);
    setPearsonSelection(!pearsonSelection);
  }

  function switchRanking(): void {
    if (allSelection) {
      setPearsonRanking(false);
      setCountRanking(true);
    } else {
      setCountRanking(!countRanking);
      setPearsonRanking(!pearsonRanking);
    }
  }

  return (
    <>
      <button
        className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 mr-4 border-blue-700 hover:border-blue-500 rounded ml-auto"
        onClick={openModal}
      >
        <AdjustmentsHorizontalIcon className="h-6 w-6" />
      </button>

      <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={closeModal}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black/25" />
          </Transition.Child>

          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4 text-center">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                  <Dialog.Title
                    as="h3"
                    className="text-lg font-medium leading-6 text-gray-900"
                  >
                    Recommendation Settings
                  </Dialog.Title>

                  <div className="flex flex-row">
                    <div className="mt-2 mr-10">
                      <label>Selection method:</label>
                      <div className="flex flex-col">
                        <label className="text-sm">All</label>
                        <Switch
                          checked={allSelection}
                          onChange={switchSelection}
                          className={`${
                            allSelection ? "bg-pink-500" : "bg-gray-300"
                          }
                                relative inline-flex h-[24px] w-[44px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2  focus-visible:ring-white/75 mb-1`}
                        >
                          <span className="sr-only">Use setting</span>
                          <span
                            aria-hidden="true"
                            className={`${
                              allSelection ? "translate-x-5" : "translate-x-0"
                            }
                                        pointer-events-none inline-block h-[20px] w-[20px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out`}
                          />
                        </Switch>
                        <label className="text-sm">Pearson</label>
                        <Switch
                          checked={pearsonSelection}
                          onChange={switchSelection}
                          className={`${
                            pearsonSelection ? "bg-pink-500" : "bg-gray-300"
                          }
                                relative inline-flex h-[24px] w-[44px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2  focus-visible:ring-white/75`}
                        >
                          <span className="sr-only">Use setting</span>
                          <span
                            aria-hidden="true"
                            className={`${
                              pearsonSelection
                                ? "translate-x-5"
                                : "translate-x-0"
                            }
                                        pointer-events-none inline-block h-[20px] w-[20px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out`}
                          />
                        </Switch>
                      </div>
                    </div>
                    <div className="mt-2">
                      <label>Ranking method:</label>
                      <div className="flex flex-col">
                        <label className="text-sm">Count</label>
                        <Switch
                          checked={countRanking}
                          onChange={switchRanking}
                          className={`${
                            countRanking ? "bg-pink-500" : "bg-gray-300"
                          }
                                relative inline-flex h-[24px] w-[44px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2  focus-visible:ring-white/75 mb-1`}
                        >
                          <span className="sr-only">Use setting</span>
                          <span
                            aria-hidden="true"
                            className={`${
                              countRanking ? "translate-x-5" : "translate-x-0"
                            }
                                        pointer-events-none inline-block h-[20px] w-[20px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out`}
                          />
                        </Switch>
                        {pearsonSelection && (
                          <label className="text-sm">Pearson-prediction</label>
                        )}
                        {pearsonSelection && (
                          <Switch
                            checked={pearsonRanking}
                            onChange={switchRanking}
                            className={`${
                              pearsonRanking ? "bg-pink-500" : "bg-gray-300"
                            }
                                relative inline-flex h-[24px] w-[44px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2  focus-visible:ring-white/75`}
                          >
                            <span className="sr-only">Use setting</span>
                            <span
                              aria-hidden="true"
                              className={`${
                                pearsonRanking
                                  ? "translate-x-5"
                                  : "translate-x-0"
                              }
                                        pointer-events-none inline-block h-[20px] w-[20px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out`}
                            />
                          </Switch>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="mt-4">
                    <button
                      type="button"
                      className="inline-flex justify-center rounded-md border border-transparent bg-blue-200 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                      onClick={() => handleSave()}
                    >
                      Save
                    </button>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
    </>
  );
}

export default Config;