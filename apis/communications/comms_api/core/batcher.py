from typing import Tuple

from guardbear.core.batcher.batcher import BatcherProcess
from guardbear.core.batcher.mux_demux import MuxDemuxManager
from guardbear.core.config.models.comms_api import BatcherConfig


def create_batcher_process(config: BatcherConfig) -> Tuple[MuxDemuxManager, BatcherProcess]:
    """Create and start a batcher process with the provided configuration.

    Parameters
    ----------
    config : BatcherConfig
        Configuration settings for the batcher process.

    Returns
    -------
    tuple(MuxDemuxManager, BatcherProcess)
        Tuple containing the MuxDemuxManager and the started BatcherProcess.
    """
    batcher_mux_demux_manager = MuxDemuxManager()
    batcher_process = BatcherProcess(
        mux_demux_queue=batcher_mux_demux_manager.get_queue(),
        config=config,
    )
    batcher_process.start()

    return batcher_mux_demux_manager, batcher_process
