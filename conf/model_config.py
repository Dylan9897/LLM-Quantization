
config = {
    "Qwen2___5-7B-Instruct":
    {
        "sample":{
            "temperature":0.8,
            "top_p":0.95,
            "batch_size":4
        },
        "inf8":{
            "max_num_seqs":8,
            "max_model_len":2048,
            "block_size":14,
            "device":"neuron",
            "quantization":"neuron_quant",
            "override_neuron_config":{
            # "cast_logits_dtype": "bfloat16",
        },
            "tensor_parallel_size":2
        }
    }
}

deep_zeek = {
    "base_url":"https://api.deepseek.com",
    "model_name":"deepseek-chat",
    "api_key":"sk-27ec8639ef674a13a7e4c59febd23dfa"
}
