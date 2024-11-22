# Copyright (c) 2024 Intel Corporation
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
import tensorflow as tf

from nncf.tensor import Tensor
from nncf.tensor import TensorDataType
from nncf.tensor.definitions import TensorBackend
from nncf.tensor.definitions import TensorDeviceType
from tests.cross_fw.test_templates.template_test_nncf_tensor import TemplateTestNNCFTensorOperators


def cast_to(x: tf.Tensor, dtype: TensorDataType) -> tf.Tensor:
    if dtype is TensorDataType.float32:
        return tf.cast(x, tf.float32)
    if dtype is TensorDataType.float16:
        return tf.cast(x, tf.float16)
    raise NotImplementedError


class TestTFNNCFTensorOperators(TemplateTestNNCFTensorOperators):
    @staticmethod
    def to_tensor(x):
        with tf.device("/CPU:0"):
            return tf.constant(x)

    @staticmethod
    def to_cpu(x):
        return x

    @staticmethod
    def cast_to(x: tf.Tensor, dtype: TensorDataType) -> tf.Tensor:
        return cast_to(x, dtype)

    @staticmethod
    def backend() -> TensorBackend:
        return TensorBackend.tf

    @staticmethod
    def device() -> TensorDeviceType:
        return TensorDeviceType.CPU

    @pytest.mark.skip("Desired slicing is not supported for TensorFlow")
    @pytest.mark.parametrize("is_tensor_indecies", (False, True))
    def test_getitem_for_indecies(self, is_tensor_indecies):
        pass

    @pytest.mark.skip("TensorFlow throws different kind of exceptions")
    @pytest.mark.parametrize(
        "val, axis, exception_type, exception_match",
        (
            ([[[[1], [2]], [[1], [2]]]], (0, 1), ValueError, "not equal to one"),
            ([[[[1], [2]], [[1], [2]]]], 42, IndexError, "out of"),
            ([[[[1], [2]], [[1], [2]]]], (0, 42), IndexError, "out of"),
        ),
    )
    def test_squeeze_axis_error(self, val, axis, exception_type, exception_match):
        pass


@pytest.mark.skipif(len(tf.config.list_physical_devices("GPU")) == 0, reason="Skipping for CPU-only setups")
class TestGPUTFNNCFTensorOperators(TemplateTestNNCFTensorOperators):
    @staticmethod
    def to_tensor(x):
        with tf.device("GPU"):
            return tf.constant(x)

    @staticmethod
    def to_cpu(x):
        with tf.device("CPU"):
            return tf.constant(x.numpy())

    @staticmethod
    def cast_to(x: tf.Tensor, dtype: TensorDataType) -> tf.Tensor:
        return cast_to(x, dtype)

    def test_device(self):
        tensor = Tensor(self.to_tensor([1]))
        assert tensor.device == TensorDeviceType.GPU

    @staticmethod
    def backend() -> TensorBackend:
        return TensorBackend.tf

    @staticmethod
    def device() -> TensorDeviceType:
        return TensorDeviceType.GPU

    @pytest.mark.skip("Desired slicing is not supported for TensorFlow")
    @pytest.mark.parametrize("is_tensor_indecies", (False, True))
    def test_getitem_for_indecies(self, is_tensor_indecies):
        pass

    @pytest.mark.skip("TensorFlow throws different kind of exceptions")
    @pytest.mark.parametrize(
        "val, axis, exception_type, exception_match",
        (
            ([[[[1], [2]], [[1], [2]]]], (0, 1), ValueError, "not equal to one"),
            ([[[[1], [2]], [[1], [2]]]], 42, IndexError, "out of"),
            ([[[[1], [2]], [[1], [2]]]], (0, 42), IndexError, "out of"),
        ),
    )
    def test_squeeze_axis_error(self, val, axis, exception_type, exception_match):
        pass
