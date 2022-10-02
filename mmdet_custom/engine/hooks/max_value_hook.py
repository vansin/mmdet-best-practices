# Copyright (c) OpenMMLab. All rights reserved.
from typing import Dict, Optional, Union

# from mmengine.utils import get_git_hash
# from mmengine.version import __version__
from mmengine.hooks.hook import Hook
from mmengine.registry import HOOKS

DATA_BATCH = Optional[Union[dict, tuple, list]]


@HOOKS.register_module()
class MaxValueHook(Hook):
    """A hook that updates runtime information into message hub.

    E.g. ``epoch``, ``iter``, ``max_epochs``, and ``max_iters`` for the
    training state. Components that cannot access the runner can get runtime
    information through the message hub.
    """

    priority = 'VERY_HIGH'

    def after_val_epoch(self,
                        runner,
                        metrics: Optional[Dict[str, float]] = None) -> None:
        """All subclasses should override this method, if they need any
        operations after each validation epoch.

        Args:
            runner (Runner): The runner of the validation process.
            metrics (Dict[str, float], optional): Evaluation results of all
                metrics on validation dataset. The keys are the names of the
                metrics, and the values are corresponding results.
        """
        if metrics is not None:
            for key, value in metrics.items():

                max_value = runner.message_hub.log_scalars[
                    f'val/{key}']._log_history.max()
                runner.message_hub.update_scalar(f'val/{key}_max', max_value)

    # def after_test_epoch(self,
    #                      runner,
    #                      metrics: Optional[Dict[str, float]] = None) -> None:
    #     """All subclasses should override this method, if they need any
    #     operations after each test epoch.

    #     Args:
    #         runner (Runner): The runner of the testing process.
    #         metrics (Dict[str, float], optional): Evaluation results of all
    #             metrics on test dataset. The keys are the names of the
    #             metrics, and the values are corresponding results.
    #     """
    #     if metrics is not None:
    #         for key, value in metrics.items():
    #             runner.message_hub.update_scalar(f'test/{key}', value)
