from manim import Scene, Table, Tex, Text, UP, DOWN, LEFT, RIGHT, Create, VGroup, Transform, Line, MovingCameraScene
from manim.utils.color import manim_colors
import itertools

class TupleTableScene(MovingCameraScene):
    def construct(self):
        sam_font = "Courier New"

        memory_size = 4
        init_set = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)]
        write_ops = [(0, 5), (0, 10), (1, 15), (0, 20), (1, 5), (2, 20)]
        num_ops = len(write_ops)
        assert(memory_size == len(init_set))

        read_set = []
        write_set = []
        final_set = init_set.copy()
        for (a_write, v_write) in write_ops:
            assert(a_write <= memory_size)
            read_tuple = final_set[a_write]
            assert(a_write == read_tuple[0])

            read_set.append(read_tuple)
            write_tuple = (a_write, v_write, read_tuple[2] + 1)
            write_set.append(write_tuple)
            final_set[a_write] = write_tuple

        self.camera.frame.scale(1.75).shift(2.5 * RIGHT)

        write_ops_label = Text("Write Ops", font=sam_font)
        write_kv_label = Text("(key, value)", font=sam_font)
        ops_labels = VGroup(write_ops_label, write_kv_label).arrange(DOWN)
        color_map = {0: manim_colors.RED, 1: manim_colors.GREEN, 2: manim_colors.BLUE, 3: manim_colors.YELLOW}
        write_ops_text = [Text(f"({a}, {v})", font=sam_font).set_color(color_map[a]) for (a, v) in write_ops]
        write_inner_ops_group = VGroup(*write_ops_text).arrange(RIGHT)
        write_ops_group = VGroup(ops_labels, write_inner_ops_group).arrange(RIGHT).to_edge(LEFT).to_edge(UP)
        self.play(Create(write_ops_group))

        horizontal_divider = Line(start=write_ops_group.get_corner(DOWN+LEFT), end=write_ops_group.get_corner(DOWN+RIGHT)).shift(DOWN)
        self.play(Create(horizontal_divider))

        init_label = Text("Init", font=sam_font)
        k_v_t_label = Text("(key, value, t=0)", font=sam_font)
        init_kvt = [Text(f"({a}, {v}, {t})", font=sam_font) for (a, v, t) in init_set]
        init_group = VGroup(init_label, k_v_t_label, *init_kvt).arrange(DOWN).next_to(horizontal_divider, DOWN).to_edge(LEFT)
        self.play(Create(init_group))

        vertical_divider_0 = Line(init_group.get_corner(UP+RIGHT), init_group.get_corner(DOWN+RIGHT)).shift(RIGHT)
        self.play(Create(vertical_divider_0))

        active_ram_group = init_group.copy()
        self.play(active_ram_group.animate.next_to(vertical_divider_0, RIGHT))
        ram_label = Text("RAM", font=sam_font)
        ram_label.move_to(active_ram_group[0])
        self.play(Transform(active_ram_group[0], ram_label))
        kvt_label = Text("(k, v, t)", font=sam_font)
        kvt_label.move_to(active_ram_group[1])
        self.play(Transform(active_ram_group[1], kvt_label))
        self.play(*[active_ram_group[i + 2].animate.set_color(color_map[a]) for i, (a, _, _) in enumerate(init_set)])

        kvt_label_2 = Text("(k, v, t)", font=sam_font)
        kvt_label_2.move_to(init_group[1])
        self.play(Transform(init_group[1], kvt_label_2))

        vertical_divider_1 = Line(active_ram_group.get_corner(UP+RIGHT), active_ram_group.get_corner(DOWN+RIGHT)).shift(RIGHT)
        self.play(Create(vertical_divider_1))

        self.play([init_group.animate.to_edge(LEFT), vertical_divider_0.animate.next_to(init_group, RIGHT), active_ram_group.animate.next_to(vertical_divider_0, RIGHT)])

        self.play(self.camera.frame.animate.scale(1.25).shift(2.5 * RIGHT))

        blank_labels_a = [Text("(_, _, _)", font=sam_font) for _ in read_set]
        blank_labels_b = [Text("(_, _, _)", font=sam_font) for _ in read_set]
        read_group = VGroup(Text("Read", font=sam_font), Text("(k, v, t)", font=sam_font), *blank_labels_a).arrange(DOWN).center()
        read_group.next_to(vertical_divider_1, RIGHT, aligned_edge=UP, buff=1)
        vertical_divider_2 = Line(read_group.get_corner(UP+RIGHT), read_group.get_corner(DOWN+RIGHT)).shift(RIGHT)
        write_group = VGroup(Text("Write", font=sam_font), Text("(k, v, t)", font=sam_font), *blank_labels_b).arrange(DOWN)
        write_group.next_to(vertical_divider_2, RIGHT, aligned_edge=UP, buff=1)
        self.play([Create(read_group), Create(vertical_divider_2), Create(write_group)])
        self.wait()

        update = lambda a, v_read, v_write, t_read, t_write, op_index: (
            self.play(write_inner_ops_group[op_index].animate.shift(0.5 * DOWN)),

            self.play([
                active_ram_group[a + 2].animate.shift(0.5 * RIGHT),
                read_group[op_index + 2].animate.shift(0.5 * RIGHT),
                write_group[op_index + 2].animate.shift(0.5 * RIGHT),
            ]),

            self.play(
                Transform(
                    read_group[op_index + 2],
                    Text(f"({a}, {v_read}, {t_read})", font=sam_font).set_color(color_map[a]).move_to(read_group[op_index + 2])
                )
            ),

            self.play(
                [
                    Transform(
                        active_ram_group[a + 2],
                        Text(f"({a}, {v_write}, {t_write})", font=sam_font).set_color(color_map[a]).move_to(active_ram_group[a + 2])
                    ),
                    Transform(
                        write_group[op_index + 2],
                        Text(f"({a}, {v_write}, {t_write})", font=sam_font).set_color(color_map[a]).move_to(write_group[op_index + 2])
                    ),
                ]
            ),

            self.play([
                active_ram_group[a + 2].animate.shift(0.5 * LEFT),
                read_group[op_index + 2].animate.shift(0.5 * LEFT),
                write_group[op_index + 2].animate.shift(0.5 * LEFT),
            ]),

            self.play(write_inner_ops_group[op_index].animate.shift(0.5 * UP)),
        )

        for op_index in range(num_ops):
            assert(read_set[op_index][0] == write_set[op_index][0])
            update(read_set[op_index][0], read_set[op_index][1], write_set[op_index][1], read_set[op_index][2], write_set[op_index][2], op_index)

        self.wait()